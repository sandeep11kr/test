# -*- coding: utf-8 -*-
import scrapy
# from scrapy_splash import SplashRequest
from ..items import RestaurantMenuItem
import re
import pandas as pd
from time import sleep
import itertools
from scrapy.utils.response import open_in_browser  


class DoordashSpider(scrapy.Spider):
    name = 'DoorDash'
    allowed_domains = ['fazolis.com']
    start_urls = ['https://order.fazolis.com/menu/austin-tx']     
    group_dict = {}
    
    custom_settings = {
        'FEED_FORMAT' : 'csv',
        'FEED_URI' : '\\ConverseNow\\Restaurant_Menu\\Fazoli Data\\Menu\\Fazoli_Website_Austin_78727_%(time)s.csv',
        'FEED_EXPORT_FIELDS' : ['id', 'category', 'name', 'description', 'price', 'calories']
    }

    
    
    # *************** Part2 From Fazoli's website *********
    def parse(self, response):
        prod_IdList = []
        customMenu_url = 'https://order.fazolis.com/product/customize?id='
        
        allCat = response.css('div h2.catName::text').extract()
        allProd = response.css('ul.Products')
        for index in range(len(allProd)):
            all_li = allProd[index].css('li')
            for item in all_li:
                prod_ID = item.attrib['data-product-id']
                prod_IdList.append(prod_ID)
                sleep(1)
                yield response.follow(customMenu_url+prod_ID, callback= self.custom_menu, cb_kwargs= {'id': prod_ID, 'cat': allCat[index]})
               
        
    def custom_menu(self, response, id, cat):
        data = RestaurantMenuItem()
        print('Sandeep: ', response.url)
        prod_ID = id
        group = []
        labelList = []
        groupStr = ""
        # mandatory_dict = {}
        requiredField = response.css('fieldset[data-is-mandatory=true]')
        for field in requiredField:
            label = field.css('legend.ProductTitle::text').get()
            if 'true' in field.css('input::attr(aria-checked)').extract():
                pass
            else:
                value = field.css('span.option-group-choice-label__name::text').extract()
                if value[0]== 'Kids Meal Beverage Choice': value = ['Kids Soft Drink', 'Milk', 'Chocolate Milk', 'Apple Juice', 'Bottled Water', 'Kids Blue Raspberry Lemon Ice', 'Kids Original Lemon Ice', 'Kids Strawberry Lemon Ice']
            # key = field.css('legend.ProductTitle::text').get()
            # key = key.strip()
            # mandatory_dict.update({key: value})
                labelList.append(label.strip())
                group.append(value)
        

        # if len(labelList)== 1: 
        #     # combo = itertools.product(*group) # For all possible combination
        #     # group = [' & '.join(tup) for tup in combo]
        #     group = [item for sublist in group for item in sublist]

            # group = [item for sublist in group for item in sublist]
            # groupStr = ";".join(group)
        
        iname = response.css('h2.product-customize__name::text').get()
        desc = response.css('div.product-customize__description::text').get()
        price = response.css('h3.product-customize__attribute--price::text').get()
        calory = response.css('h3.product-customize__attribute--calories::text').get()

        data['id'] = prod_ID
        data['category'] = cat
        data['name'] = iname
        data['description'] = desc.strip()
        data['price'] = price.strip() if price is not None else ""
        data['calories'] = calory.strip() if calory is not None else ""
        #data['required_combo'] = group if len(group)>0 else ""
        # data['required_combo'] = mandatory_dict if len(mandatory_dict)>0 else ""
        #yield data
        if len(group) == 0 :
            yield data

        elif len(group)== 1:
            # data['name'] = iname+':'+groupStr
            # yield data
            group = [item for sublist in group for item in sublist]
            for elem in group:
                data['name'] = iname+'=>'+elem
                yield data

        elif len(group)> 1:
            groupDict = {}
            for index in range(len(labelList)):
                groupDict[labelList[index]] = group[index]
            data['name'] = iname+'=>'+str(groupDict)
            print('NOS: ', groupDict)
            yield data

            
            
        
        
