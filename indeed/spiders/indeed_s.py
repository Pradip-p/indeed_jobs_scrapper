import scrapy
import js2xml
from time import sleep
import dateparser
from fake_useragent import UserAgent

class ExampleSpider(scrapy.Spider):
    name = "indeed"
    allowed_domains = ["au.indeed.com"]
    ua = UserAgent()

    def start_requests(self):
        url = 'https://au.indeed.com/jobs?q=nurse&l=Australia'
        
        yield scrapy.Request(url, callback=self.parse,
                            headers= {f"User-Agent":self.ua.random},
                            meta={
                                "playwright": True
                             })
                            
    def parse(self, response):
        try:
            script = response.css('#mosaic-data::text').get('')
            parsed = js2xml.parse(script)
            results = js2xml.jsonlike.make_dict(
                parsed.xpath('//property[@name="results"]/array')[0])
            for job in results:
                get_job = self.parse_job(job)
                print(get_job)
                # yield get_job
                
        except:
            sleep(1)
            pass
    
    def parse_job(self, job_dict):

        job = {}
        jobkey = str(job_dict.get('jobkey'))
        job['jobkey'] = jobkey

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
                job['Date_Posted'] = dateparser.date('30 days ago').date()
        else:

            job['Date_Posted'] = str(date_posted.date())

        job['Urgent_Hire'] = job_dict.get('urgentlyHiring')

        job['Salary'] = job_dict.get('salarySnippet', {}).get('text')
        job['hot_job'] = 'no'
        job['Company'] = job_dict.get('company')

        job['Job_Type'] = ' | '.join(job_dict.get('jobTypes'))

        d_link = 'https://au.indeed.com/rc/clk?jk={jobkey}&atk='
        print(job)
        return scrapy.Request(d_link.format(jobkey=jobkey), headers={'User-Agent': self.ua},
                    meta={'job': job}, callback=self.direct_link)

    def direct_link(self, response):
        if response.status == 400:
            print("")
        else:
            job = response.meta.get('job')
            job['Direct_Link'] = response.url
            yield job
        
