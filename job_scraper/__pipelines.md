# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from supabase import create_client, Client
# import sqlalchemy as db
import hashlib
import json
from urllib.parse import urlparse
# from sqlalchemy import exc
# from scrapy.exceptions import DropItem

#class JobScraperPipeline:
#    def __init__(self):
#         self.engine = db.create_engine("mysql+pymysql://nurseseeking:G9k4pe@65.108.59.72:30306/alljobs")
#         self.connection = self.engine.connect()
#         self.metadata = db.MetaData()
#         self.jobs = db.Table('jobs', self.metadata, autoload=True, autoload_with=self.engine)
#         self.review_jobs = db.Table('review_jobs', self.metadata, autoload=True, autoload_with=self.engine)
#
#     def process_item(self, item, spider):
#         hash_dict = {'Link':item.get('Link'),'Job_Title':item.get('Job_Title'),'Company':item.get('Comapny')}
#         binary = json.dumps(hash_dict).encode('utf-8')
#         hashed_key = hashlib.sha1(binary).hexdigest()
#
#         item['id'] = hashed_key
#
#         insert = db.insert(self.jobs)
#
#         try:
#            if 'nurse' in item['Job_Title'].lower():
#                 self.connection.execute(insert,[item])
#            else:
#                self.connection.execute(db.insert(self.review_jobs),[item])
#         except exc.IntegrityError:
#             raise DropItem("Duplicate item found: %s" % hashed_key)
#
#         return item
class Supabase:

    def __init__(self):
        self.url = "https://nskong.send.rodeo"
        self.key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyAgCiAgICAicm9sZSI6ICJhbm9uIiwKICAgICJpc3MiOiAic3VwYWJhc2UtZGVtbyIsCiAgICAiaWF0IjogMTY0MTc2OTIwMCwKICAgICJleHAiOiAxNzk5NTM1NjAwCn0.dc_X5iR_VP_qT0zsiyj_I_OZ2T9FtRU2BBNWN8Bu4GE"
        self.supabase: Client = create_client(self.url, self.key)

    def process_item(self, item, spider):
        hash_dict = {'Link':item.get('Link'),'Job_Title':item.get('Job_Title'),'Company':item.get('Company')}
        binary = json.dumps(hash_dict).encode('utf-8')
        hashed_key = hashlib.sha1(binary).hexdigest()

        if 'jobkey' not in list(item.keys()):

            item['jobkey'] = hashed_key
        domain = urlparse(item.get('Direct_Link')).netloc

        data = self.supabase.table("jobs").insert({
            "uuid": item['jobkey'],
            "job_title": item['Job_Title'],
            "scraped_link": item['Link'],
            "apply_link": item['Direct_Link'],
            "company": item['Company'],
            "address": item['Address'],
            "state": item['state'],
            "date_posted": item['Date_Posted'],
            "job_type": item['Job_Type'],
            "hot_job": item['hot_job'],
            "salary": item['Salary'],
            "urgent_hire": item['Urgent_Hire'],
            "logo_link":domain
        }).execute()

        assert len(data.data) > 0

        return item