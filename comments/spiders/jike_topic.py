# -*- coding: utf-8 -*-
import scrapy
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


class JikeTopicSpider(scrapy.Spider):
    name = 'jike_topic'
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