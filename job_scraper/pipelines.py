# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import hashlib
import json
from urllib.parse import urlparse


class Firebase:

    def __init__(self):
        self.cred = credentials.Certificate({
        }
        )
        self.default_app = firebase_admin.initialize_app(self.cred)
        self.db = firestore.client()

    def process_item(self, item, spider):
        hash_dict = {'Link': item.get('Link'), 'Job_Title': item.get(
            'Job_Title'), 'Company': item.get('Company')}
        binary = json.dumps(hash_dict).encode('utf-8')
        hashed_key = hashlib.sha1(binary).hexdigest()

        if 'jobkey' not in list(item.keys()):
            item['jobkey'] = hashed_key

        domain = urlparse(item.get('Direct_Link')).netloc

        print("before adding to firestore")

        data = self.db.collection("jobs").add({
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
            "logo_link": domain
        })

        print("data ", data)

        assert len(data) > 0

        return item
