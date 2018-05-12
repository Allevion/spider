# -*- coding: utf-8 -*-
import scrapy
import re
import json
from scrapy.http import Request
from comments.items import TopicItem
#
headers = {
'Accept-Language': 'zh-cn',
'Accept-Encoding': 'br, gzip, deflate',
'Content-Type': 'application/json',
'User-Agent': '%E5%8D%B3%E5%88%BB/1107'
}

topics = ['RECOMMENDATION','FUN','ENTERTAINMENT','LIFE','MUSIC','SPORT','ANIMATION','CULTURE',
'NEWS','TECH','GAME','FINANCE']

# topics = ['FUN','ENTERTAINMENT']


class JikeSpider(scrapy.Spider):
    name = 'jike'
    allowed_domains = ['jike.ruguoapp.com']


    # test = True
    def start_requests(self):
        for topic in topics:
            topic_body = {}
            topic_body['categoryAlias'] = topic
            request = Request(url='http://app.jike.ruguoapp.com/1.0/topics/recommendation/list', method='POST',
                      body=json.dumps(topic_body),
                      headers=headers, callback=self.parse_topic)
            request.meta['topic'] = topic
            yield request
        #
        # req_body = {}
        # req_body['topic'] =  '5752cb471c0d051200ba0a1f'
        # req_body['limit'] =  '100'
        # req_body['loadMoreKey'] =  '5a8797443652c300108e81cf'
        # yield Request(url='http://app.jike.ruguoapp.com/1.0/messages/history',method='POST',
        #                   body=req_body,
        #                   headers=headers,callback=self.parse)

    def parse_topic(self, response):
        topics = json.loads(response.text)
        if topics['data'] and len(topics['data']) > 0:
            for topic in topics['data']:
                topicItem = TopicItem()
                topicItem['topic'] = topic
                yield topicItem
        if topics['loadMoreKey']:

            topic_body = {}
            topic_body['categoryAlias'] = response.meta['topic']
            topic_body['loadMoreKey'] = topics['loadMoreKey']
            request = Request(url='http://app.jike.ruguoapp.com/1.0/topics/recommendation/list', method='POST',
                              body=json.dumps(topic_body),
                              headers=headers, callback=self.parse_topic)
            request.meta['topic'] = response.meta['topic']
            yield request
        pass

