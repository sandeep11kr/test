# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RestaurantMenuItem(scrapy.Item):
    # define the fields for your item here like:
    
    id = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    description = scrapy.Field()
    calories = scrapy.Field()
    category = scrapy.Field()
    required_combo = scrapy.Field()
    address = scrapy.Field()
    city = scrapy.Field()
    state = scrapy.Field()
    postal = scrapy.Field()
    url = scrapy.Field()
    