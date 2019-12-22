# -*- coding: utf-8 -*-
import os
import scrapy
from ..items import RestaurantMenuItem


class FazoliLocSpider(scrapy.Spider):
    name = 'fazoli_Loc'
    allowed_domains = ['fazolis.com']
    start_urls = ['https://locations.fazolis.com/']

    def __init__(self):
        self.fazoli = RestaurantMenuItem()

    custom_settings = {
        'FEED_FORMAT' : 'csv',
        'FEED_URI' : os.path.join('Fazoli Data', 'Fazoli_Address with url.csv'),
        'FEED_EXPORT_FIELDS' : ['address', 'city', 'state', 'postal', 'url']
    }

    #fazoli = RestaurantMenuItem()

    def parse(self, response):
        state_urls = response.css('a.c-directory-list-content-item-link::attr(href)').extract()
        for href in state_urls:
            yield response.follow(href, callback= self.parse_city)

    def parse_city(self, response):
        city_urls = response.css('a.c-directory-list-content-item-link::attr(href)').extract()
        
        if len(city_urls)==0 :
            for data in response.css('div.split') or response.css('article.Teaser--directory'):
                add = data.css('span.c-address-street-1::text').get()
                add2 = data.css('span.c-address-city::text').get()
                states = data.css('abbr::attr(title)').get()
                postal = data.css('span.c-address-postal-code::text').get()
                url = response.css('a.location-info-order-button::attr(href)').get() or data.css('div.Teaser-order').css('a::attr(href)').get()
                self.fazoli['address']= add
                self.fazoli['city']= add2
                self.fazoli['state']= states
                self.fazoli['postal']= postal
                self.fazoli['url']= url
                yield self.fazoli
        else:
            for href in city_urls:
                yield response.follow(url= href, callback= self.parse_data)
            

    def parse_data(self, response):       #Address of Restaurant 
        for data in response.css('div.split') or response.css('article.Teaser--directory'):
            add = data.css('span.c-address-street-1::text').get()
            add2 = data.css('span.c-address-city::text').get()
            states = data.css('abbr::attr(title)').get()
            postal = data.css('span.c-address-postal-code::text').get()
            url = response.css('a.location-info-order-button::attr(href)').get() or data.css('div.Teaser-order').css('a::attr(href)').get()
            self.fazoli['address']= add
            self.fazoli['city'] = add2
            self.fazoli['state']= states
            self.fazoli['postal']= postal
            self.fazoli['url']= url
            yield self.fazoli