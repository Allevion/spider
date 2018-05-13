# -*- coding: utf-8 -*-
import scrapy
import re
import json
from scrapy.http import Request
from comments.items import TopicItem
from comments.items import TimelineItem
from comments.items import CommentItem
import pymongo
import requests
#

REQUEST_TPYE_TOPIC = 'TOPIC'
REQUEST_TPYE_TIMELINE = 'TIMELINE'
REQUEST_TPYE_COMMENT = 'COMMENT'

PRIMATY_COMMENT_COUNT = 50# 暂时不加翻页
COMMENT_COUNT = 20# 暂时不加翻页

headers = {
'Accept-Language': 'zh-cn',
'Accept-Encoding': 'br, gzip, deflate',
'Content-Type': 'application/json',
'User-Agent': '%E5%8D%B3%E5%88%BB/1107',
'App-Version': '4.4.0',
'BundleID': 'com.ruguoapp.jike'
}

categoryAlias = ['RECOMMENDATION','FUN','ENTERTAINMENT','LIFE','MUSIC','SPORT','ANIMATION','CULTURE',
'NEWS','TECH','GAME','FINANCE']

# categoryAlias = ['FUN']

class JikeSpider(scrapy.Spider):
    name = 'jike'
    allowed_domains = ['jike.ruguoapp.com']

    def __init__(self):
        clinet = pymongo.MongoClient("localhost", 27017)
        db = clinet["comments"]


    def start_requests(self):
        for categoryAlia in categoryAlias:
            yield self.topic_request(categoryAlia)



    def topic_request(self, categoryAlia, loadMoreKey=None):
        request_body = {}
        request_body['categoryAlias'] = categoryAlia
        request_body['limit'] = 50
        if loadMoreKey:
            request_body['loadMoreKey'] = loadMoreKey
        request = Request(url='http://app.jike.ruguoapp.com/1.0/topics/recommendation/list', method='POST',
                          body=json.dumps(request_body),
                          headers=headers, callback=self.parse_topic)
        request.meta['categoryAlia'] = categoryAlia
        return request


    def timeline_request(self, topic_id, loadMoreKey=None):
        request_body = {}
        request_body['topic'] = topic_id
        request_body['limit'] = 50
        if loadMoreKey:
            request_body['loadMoreKey'] = loadMoreKey
        request = Request(url='http://app.jike.ruguoapp.com/1.0/messages/history', method='POST',
                          body=json.dumps(request_body),
                          headers=headers, callback=self.parse_timeline)
        request.meta['topic'] = topic_id
        return request

    def commemt_request(self, targetId,targetType, loadMoreKey=None):
        request_body = {}
        request_body['targetId'] = targetId
        request_body['limit'] = PRIMATY_COMMENT_COUNT
        request_body['targetType'] = targetType

        # 暂时不加翻页
        # if loadMoreKey:
        #     request_body['loadMoreKey'] = loadMoreKey
        request = Request(url='http://app.jike.ruguoapp.com/1.0/comments/listPrimary', method='POST',
                          body=json.dumps(request_body),
                          headers=headers, callback=self.parse_comment)
        request.meta['targetId'] = targetId
        return request

    def commemt_reply_request(self, comment, loadMoreKey=None):
        request_body = {}
        request_body['primaryCommentId'] = comment['id']
        request_body['limit'] = COMMENT_COUNT
        request_body['targetType'] = comment['targetType']
        request_body['order'] = 'LIKES'
        # 暂时不加翻页
        # if loadMoreKey:
        #     request_body['loadMoreKey'] = loadMoreKey
        request = Request(url='http://app.jike.ruguoapp.com/1.0/comments/list', method='POST',
                          body=json.dumps(request_body),
                          headers=headers, callback=self.parse_comment_reply)
        # 暂时不加翻页
        # request.meta['primaryCommentId'] = primaryCommentId
        # request.meta['targetType'] = targetType
        request.meta['comment'] = comment
        return request


    def parse_topic(self, response):
        topics = json.loads(response.text)
        if topics['data'] and len(topics['data']) > 0:
            for topic in topics['data']:
                topicItem = TopicItem()
                topicItem['topic'] = topic
                if topic['subscribersCount'] > 100:  # 关注小于10000数据舍弃
                    yield topicItem
                    yield self.timeline_request(topic['id'])
        if topics['loadMoreKey']:
            yield self.topic_request(response.meta['categoryAlia'],topics['loadMoreKey'])
        pass

    def parse_timeline(self, response):
        timelines = json.loads(response.text)
        if timelines['data'] and len(timelines['data']) > 0:
            for timeline in timelines['data']:
                if timeline['commentCount'] > 10 and timeline['likeCount'] > 10 :# 评论、点赞小于10数据舍弃，repostCount转发暂不考虑

                    item = TimelineItem()
                    item['timeline'] = timeline
                    yield item
                    yield self.commemt_request(timeline['id'],timeline['type'])
        if timelines['loadMoreKey']:
            yield self.timeline_request(response.meta['topic'],timelines['loadMoreKey'])
        pass

    def parse_comment(self, response):
        comments = json.loads(response.text)
        if comments['data'] and len(comments['data']) > 0:
            for comment in comments['data']:
                if comment['replyCount'] == 0:
                    item = CommentItem()
                    item['primaryComment'] = comment
                    yield item
                else:
                    if comment['likeCount'] >= 0 and comment['replyCount'] >= 0 :# 回复、点赞小于1数据舍弃


                    # if True:
                        # item = CommentItem()
                        # item['primaryComment'] = comment
                        yield self.commemt_reply_request(comment)

        # if timelines['loadMoreKey']:
        #     yield self.timeline_request(response.meta['topic'],timelines['loadMoreKey'])
        pass

    def parse_comment_reply(self, response):
        comments = json.loads(response.text)
        item = CommentItem()
        item['primaryComment'] = response.meta['comment']
        item['commentReply'] = comments['data']
        yield item

