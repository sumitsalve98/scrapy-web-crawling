# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WebcrawlCoursesItem(scrapy.Item):
    # define the fields for your item here like:
    Title = scrapy.Field()
    Short_Description = scrapy.Field()
    Description = scrapy.Field()
    Key_skills = scrapy.Field()
    Prerequitsites = scrapy.Field()
    syllabus = scrapy.Field()
    Price = scrapy.Field()

