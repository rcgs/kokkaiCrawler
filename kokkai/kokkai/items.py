# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class kokkaiItem(scrapy.Item):
    # define the fields for your item here like:
    kokkai_link = scrapy.Field()
    opac_link = scrapy.Field()
    shosi_id = scrapy.Field()
    
    pass
