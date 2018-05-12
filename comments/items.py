# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import pymongo



from scrapy import Item, Field


class TopicItem(Item):
    topic = Field()

class TimelineItem(Item):
    timeline = Field()

class CommentItem(Item):
    primaryComment = Field()
    comment = Field()
