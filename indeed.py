import json
import hashlib
import logging
import pymongo
from get_logo import get_logo_url
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import dateparser
import js2xml
from selenium.common.exceptions import TimeoutException
from lib.user_agent import get_user_agent
from urllib.parse import urlparse, urlunparse


class IndeedScraper:

    def __init__(self, collection_name):
        self.base_url = 'https://au.indeed.com/jobs?q=nurse&l=Australia&start={}'
        self.start_urls = [self.base_url.format(i) for i in range(1, 660, 10)]
        self.collection_name = collection_name  # Added collection_name as an instance variable
        self.client = pymongo.MongoClient('')
        self.db = self.client['']
        self.collection = self.db[self.collection_name]
        self.driver = None  # Initialize the driver as an instance variable

    def get_actual_job_link(self, url):
        try:
            self.driver.get(url)
            final_redirected_url = self.driver.current_url  # This gets the current URL after any redirects
            parsed_url = urlparse(final_redirected_url)
            modified_url = urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, '', '', ''))


        except Exception as e:
            print(f"Error getting actual job link: {e}")
            modified_url = None

        return modified_url

    def initialize_driver(self):
        options = Options()
        options.add_argument('--headless')  # use headless browser mode
        # Set user-agent and window size
        user_agent = get_user_agent('random')  # Assuming get_user_agent is defined elsewhere
        options.add_argument(f"user-agent={user_agent}")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        options.add_argument("--window-size=1920x1080")

        # Disable browser automation detection
        options.add_argument("--disable-blink-features=AutomationControlled")

        # Enable loading of images
        # prefs = {"profile.managed_default_content_settings.images": 2}
        # options.add_experimental_option("prefs", prefs)

        # Update the path to your ChromeDriver executable
        self.driver = webdriver.Chrome(options=options)

    def close_driver(self):
        if self.driver:
            self.driver.quit()

    def parse_jobs(self, soup):
        if soup:
            script_tag = soup.find('script', {'id': 'mosaic-data'})

            if script_tag:
                script = script_tag.text
                parsed = js2xml.parse(script)
                results = js2xml.jsonlike.make_dict(parsed.xpath('//property[@name="results"]/array')[0])

                return results
            else:
                return None
        else:
            print('Soup not found')

    def run(self):
        try:
            self.initialize_driver()

            for url in self.start_urls:
                self.driver.get(url)

                # Wait for the page to load
                try:
                    element = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.ID, 'mosaic-data'))
                    )
                    # Your code to interact with the element once it's present
                except TimeoutException:
                    print("Timeout: The element with ID 'mosaic-data' was not found within the specified time.")
                    # Handle the timeout situation as needed, you may choose to retry, log, or raise an exception.

                soup = BeautifulSoup(self.driver.page_source, 'html.parser')
                parse_job = self.parse_jobs(soup)

                if parse_job:
                    for job_dict in parse_job:
                        job = {}
                        jobkey = str(job_dict.get('jobkey'))
                        job['jobkey'] = jobkey
                        # Populate other job details here
                        job['Job_Title'] = job_dict.get('title')

                        job['Link'] = 'https://au.indeed.com/viewjob?jk=' + jobkey

                        job['Address'] = job_dict.get('formattedLocation')
                        job['state'] = job_dict.get('moreLinks', {}).get('locationName')
                        frelative_time = job_dict.get('formattedRelativeTime')
                        date_posted = dateparser.parse(frelative_time)
                        if date_posted == None:
                            if 'Just' in frelative_time:
                                job['Date_Posted'] = str(
                                    dateparser.parse('1 minutes ago').date())
                            else:
                                job['Date_Posted'] = str(
                                    dateparser.parse('30 days ago').date())
                        else:
                            job['Date_Posted'] = str(date_posted.date())

                        job['Urgent_Hire'] = job_dict.get('urgentlyHiring')

                        job['Salary'] = job_dict.get('salarySnippet', {}).get('text')
                        job['hot_job'] = 'no'
                        job['Company'] = job_dict.get('company')

                        job['Job_Type'] = ' | '.join(job_dict.get('jobTypes'))
                        d_link = 'https://au.indeed.com/rc/clk?jk={jobkey}&atk='.format(jobkey=jobkey)
                        job['Direct_Link'] = d_link

                        ##############Get the actual link from the
                        job['apply_link'] = self.get_actual_job_link(d_link)

                        job['collection_name'] = self.collection_name

                        # Generate a unique key for the job
                        hash_dict = {'Link': job.get('Link'), 'Job_Title': job.get('Job_Title'), 'Company': job.get('Company')}
                        binary = json.dumps(hash_dict).encode('utf-8')
                        hashed_key = hashlib.sha1(binary).hexdigest()

                        # If 'jobkey' is not present in the item, set it to the hashed key
                        job['jobkey'] = job.get('jobkey', hashed_key)

                        # Check if the jobkey already exists in the database
                        existing_job = self.collection.find_one({"uuid": job['jobkey']})

                        if existing_job:
                            # Job already exists, do something if needed
                            print(f"Job with key {jobkey} already exists in the collection '{self.collection_name}'. Skipping...")
                            logging.debug(f"Job with key {jobkey} already exists in the collection '{self.collection_name}'. Skipping...")
                        else:
                            if "i work for nsw" in job['Company'].lower() or "local health district" in job['Company'].lower():
                                logo_url = get_logo_url('nsw health')
                            else:
                                logo_url = get_logo_url(job['Company'])

                            # Job doesn't exist, insert it into the collection
                            domain = urlparse(job.get('Direct_Link')).netloc
                            data = self.collection.insert_one({
                                "uuid": job['jobkey'],
                                "job_title": job['Job_Title'],
                                "scraped_link": job['Link'],
                                "apply_link": job['apply_link'],
                                "company": job['Company'],
                                "address": job['Address'],
                                "state": job['state'],
                                "date_posted": job['Date_Posted'],
                                "job_type": job['Job_Type'],
                                "hot_job": job['hot_job'],
                                "salary": job['Salary'],
                                "urgent_hire": job['Urgent_Hire'],
                                "logo_link": domain,
                                "logo_url" : logo_url
                            })

                            print(f'Added to the collection "{job}" in the MongoDB.........................')

        except Exception as e:
            print(f"Error in the run method: {e}")
        finally:
            self.close_driver()


