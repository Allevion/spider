# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from comments.items import TopicItem
from comments.items import TimelineItem
from comments.items import CommentItem

class TopicPipeline(object):
    def __init__(self):
        clinet = pymongo.MongoClient("localhost", 27017)
        db = clinet["jike"]
        self.jike = db["jike_topic"]

    def process_item(self, item, spider):
        if isinstance(item, TopicItem):
            try:
                topic = item['topic']
                self.jike.update_one({'_id': topic['id']}, {'$set': topic}, upsert=True)
                return
            except Exception:
                pass
        return item


class TimelinePipeline(object):
    def __init__(self):
        clinet = pymongo.MongoClient("localhost", 27017)
        db = clinet["jike"]
        self.jike = db["jike_timeline"]

    def process_item(self, item, spider):
        if isinstance(item, TimelineItem):
            try:
                timeline = item['timeline']
                self.jike.update_one({'_id': timeline['id']}, {'$set': timeline}, upsert=True)
                return
            except Exception:
                pass
        return item

class CommentsPipeline(object):
    def __init__(self):
        clinet = pymongo.MongoClient("localhost", 27017)
        db = clinet["jike"]
        self.jike = db["jike_comment"]

    def process_item(self, item, spider):
        if isinstance(item, CommentItem):
            try:
                comment = item['primaryComment']
                if item['commentReply']:
                    comment[u'commentReply'] = item['commentReply']
                self.jike.update_one({'_id': comment['id']}, {'$set': comment}, upsert=True)
                return
            except Exception:
                pass
        return item