# -*- coding: utf-8 -*-
from scrapy import Request, Spider
import js2xml
import dateparser
from scrapy.linkextractors import LinkExtractor
from time import sleep
from fake_useragent import UserAgent, VERSION, FakeUserAgentError
from ..filters import indeed


class IndeedSpider(Spider):
    
    name = 'indeed'

    start_urls = indeed
    
    link_extractor = LinkExtractor(restrict_css=('.pagination-list a'))
    print(VERSION)
    # try:
    ua = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.2 (KHTML, like Gecko) Chrome/22.0.1216.0 Safari/537.2"
    # except FakeUserAgentError:
    #     pass
    custom_settings = {
        'DOWNLOAD_DELAY': 2,
        'CONCURRENT_REQUESTS': 1,
        'ROBOTSTXT_OBEY': False
    }

    def parse(self, response):
        job_types = response.css(
            '#filter-jobtype-menu>li a::attr(href)').getall()
        for jt in job_types:
            abs_url = response.urljoin(jt)
            yield Request(abs_url, callback=self.parse_jobs, headers={'User-Agent': self.ua}, dont_filter=True)

    def parse_jobs(self, response):
        try:
            script = response.css('#mosaic-data::text').get('')
            parsed = js2xml.parse(script)
            results = js2xml.jsonlike.make_dict(
                parsed.xpath('//property[@name="results"]/array')[0])
            for job in results:
                get_job = self.parse_job(job)
                yield get_job
        except:
            sleep(1)
            pass
        #            print('Sleeping for 1 sec >>>>>>>>>>>>>>')
        #            for item in self.parse_jobs(response):
        #                yield item

        for link in self.link_extractor.extract_links(response):
            yield Request(link.url, callback=self.parse_jobs,
                          headers={'User-Agent': self.ua})

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

        return Request(d_link.format(jobkey=jobkey), headers={'User-Agent': self.ua},
                       meta={'job': job}, callback=self.direct_link)

    def direct_link(self, response):
        if response.status == 400:
            print("")
        else:
            job = response.meta.get('job')
            job['Direct_Link'] = response.url
            yield job
