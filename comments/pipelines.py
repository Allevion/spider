# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from comments.items import TopicItem

class CommentsPipeline(object):
    def __init__(self):
        clinet = pymongo.MongoClient("localhost", 27017)
        db = clinet["comments"]
        self.jike = db["jike"]

    def process_item(self, item, spider):
        if isinstance(item, TopicItem):
            try:
                topic = item['topic']
                self.jike.update_one({'_id': topic['id']}, {'$set': topic}, upsert=True)
            except Exception:
                pass
        return item
