# -*- coding: utf-8 -*-
import scrapy
from ..items import RestaurantMenuItem
import re, os
import pandas as pd
from time import sleep
import itertools
from scrapy.utils.response import open_in_browser  

class RedataSpider(scrapy.Spider):
    name = 'reData'
    allowed_domains = ['fazoli.com']
    #start_urls = ['https://order.fazolis.com/menu/austin-tx'] 
    
    def __init__(self, url= None, city= None, path= None):
        self.url = url
        self.city = city
        path = os.path.join(path, 'website')
        if not os.path.exists(path):
            os.mkdir(path)
        self.path = path
    
    custom_settings = {
        'FEED_FORMAT' : 'csv',
        'FEED_URI' : os.path.join('%(path)s', 'Fazoli_Website_%(city)s.csv'),
        #'FEED_URI' : os.path.join('Website', 'Fazoli Data', 'Menu', 'Fazoli_Website_%(city)s.csv'),
        'FEED_EXPORT_FIELDS' : ['id', 'category', 'name', 'description', 'price', 'calories', 'url'],
    }

    def start_requests(self):
        yield scrapy.Request(self.url, dont_filter= True)



    # *************** From Fazoli's website with rule of 10/12 *********
    def parse(self, response):
        data = RestaurantMenuItem()
        FIXED_KEY = ['add a veggie', 'add a meat', 'side of sauce', 'family side of sauce']
        prod_IdList = []
        customMenu_url = 'https://order.fazolis.com/product/customize?id='
        
        allCat = response.css('div h2.catName::text').extract()
        allProd = response.css('ul.Products')
        for index in range(len(allProd)):
            all_li = allProd[index].css('li')
            for item in all_li:
                prod_ID = item.attrib['data-product-id']
                iname = item.css('span.product__name::text').get()
                desc = item.css('span.product__description::text').get()
                price = item.css('span.product__attribute--price::text').get()
                calory = item.css('span.product__attribute--calorie-label::text').get()
                data['id'] = prod_ID
                data['name'] = iname
                data['description'] = desc.strip()
                data['category'] = allCat[index]
                data['price'] = price.strip() if price is not None else ""
                data['calories'] = calory.strip() if calory is not None else ""
                data['url'] = response.url
                
                if iname.lower() in FIXED_KEY:
                    print(iname)
                    yield response.follow(customMenu_url+prod_ID, callback= self.custom_menu, dont_filter= True, cb_kwargs= {'id': prod_ID, 'cat': allCat[index], 'reqURL': response.url})    
                else:
                    yield data
                prod_IdList.append(prod_ID)
                sleep(1)
                #yield response.follow(customMenu_url+prod_ID, callback= self.custom_menu, cb_kwargs= {'id': prod_ID, 'cat': allCat[index]})
               
        
    def custom_menu(self, response, id, cat, reqURL):
        data = RestaurantMenuItem()
        print('Sandeep: ', response.url)
        prod_ID = id
        requiredField = response.css('fieldset[data-is-mandatory=true]')
        for field in requiredField:
            value = field.css('span.option-group-choice-label__name::text').extract()
            
        iname = response.css('h2.product-customize__name::text').get()
        desc = response.css('div.product-customize__description::text').get()
        price = response.css('h3.product-customize__attribute--price::text').get()
        calory = response.css('h3.product-customize__attribute--calories::text').get()

        data['id'] = prod_ID
        data['category'] = cat
        #data['name'] = iname
        data['description'] = desc.strip()
        data['price'] = price.strip() if price is not None else ""
        data['calories'] = calory.strip() if calory is not None else ""
        data['url'] = reqURL
        
        for elem in value:
            data['name'] = iname+'=>'+elem
            yield data
        