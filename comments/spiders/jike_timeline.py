# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy.http import Request
import pymongo
from comments.items import TimelineItem

headers = {
'Accept-Language': 'zh-cn',
'Accept-Encoding': 'br, gzip, deflate',
'Content-Type': 'application/json',
'User-Agent': '%E5%8D%B3%E5%88%BB/1107'
}


class JikeTimelineSpider(scrapy.Spider):
    name = 'jike_timeline'
    allowed_domains = ['jike.ruguoapp.com']

    def getRequest(self,topic_id,loadMoreKey):
        request_body = {}
        request_body['topic'] = topic_id
        request_body['limit'] = 50
        if loadMoreKey:
            request_body['loadMoreKey'] = loadMoreKey
        request = Request(url='http://app.jike.ruguoapp.com/1.0/messages/history', method='POST',
                          body=json.dumps(request_body),
                          headers=headers, callback=self.parse)
        request.meta['topic'] = topic_id
        return request

    def start_requests(self):
        clinet = pymongo.MongoClient("localhost", 27017)
        db = clinet["comments"]
        jike = db['jike']

        for topic in jike.find():
            yield self.getRequest(topic['_id'],None)

    def parse(self, response):
        timelines = json.loads(response.text)
        if timelines['data'] and len(timelines['data']) > 0:
            for timeline in timelines['data']:
                item = TimelineItem()
                item['timeline'] = timeline
                yield item
        if timelines['loadMoreKey']:
            yield self.getRequest(response.meta['topic'],timelines['loadMoreKey'])
        pass
