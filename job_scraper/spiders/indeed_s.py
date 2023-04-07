# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from scrapy import Request, Spider
import js2xml
import dateparser
from ..filters import indeed
import cloudscraper


class IndeedSpider(Spider):
    name = 'indeed'

    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        'CONCURRENT_REQUESTS': 32,
        'ROBOTSTXT_OBEY': False,
    }

    count = 0

    url = 'http://example.com/'

    def start_requests(self):
        next_url = indeed[0]
        yield Request(self.url, self.parse, meta={'next_url': next_url}, dont_filter=True)

    def parse(self, response):
        # url = response.meta['next_url']
        for i in range(1,66):
            self.count = self.count + 10
            url = 'https://au.indeed.com/jobs?q=nurse&l=Australia&start={}'.format(self.count)
    
            soup = self.get_soup(url)

            parse_job = self.parse_jobs(soup)

            for job in parse_job:
                yield Request(self.url, self.parse_again, meta={"job": job}, dont_filter=True)

        # next_url = get_next_page_url(soup)
        # if next_url:

        #     del url
        #     url = ''
        #     yield Request(self.url, callback=self.parse, meta={'next_url': next_url}, dont_filter=True)

    def parse_again(self, response):
        res = response.meta['job']
        yield Request('http://example.com/', self.parse_job, meta={"job": res}, dont_filter=True)

    def parse_job(self, response):
        job_dict = response.meta['job']
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
                job['Date_Posted'] = str(
                    dateparser.parse('30 days ago').date())
        else:

            job['Date_Posted'] = str(date_posted.date())

        job['Urgent_Hire'] = job_dict.get('urgentlyHiring')

        job['Salary'] = job_dict.get('salarySnippet', {}).get('text')
        job['hot_job'] = 'no'
        job['Company'] = job_dict.get('company')

        job['Job_Type'] = ' | '.join(job_dict.get('jobTypes'))
        d_link = 'https://au.indeed.com/rc/clk?jk={jobkey}&atk='.format(
            jobkey=jobkey)
        job['Direct_Link'] = d_link

        yield job


    def get_soup(self,url):
        print("*"*100, url)
        # scraper = cloudscraper.create_scraper(delay=10)
        scraper = cloudscraper.create_scraper(disableCloudflareV1=True)
        response = scraper.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        return soup


    def parse_jobs(self, soup):
        script = soup.find('script', {'id': 'mosaic-data'}).text

        parsed = js2xml.parse(script)
        results = js2xml.jsonlike.make_dict(
            parsed.xpath('//property[@name="results"]/array')[0])

        return results


# def get_next_page_url(soup):
#     next_tag = soup.find('a', {'data-testid': 'pagination-page-next'})
#     if next_tag:
#         next_url = 'https://au.indeed.com'+next_tag.attrs['href']
#         return next_url
