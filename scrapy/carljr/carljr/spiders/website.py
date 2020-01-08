# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy.utils.response import open_in_browser
import pandas as pd

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



class WebsiteSpider(scrapy.Spider):
    name = 'website'
    allowed_domains = ['carlsjr.com']
    start_urls = ['https://www.carlsjr.com/menu-sitemap']

    def __init__(self):
        self.desc_DF = pd.DataFrame(columns= ['Category', 'Sub Category', 'Name', 'Description', 'Nutritional value', 'Allergens'])

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome(executable_path= "chromedriver", options= chrome_options)

    def parse(self, response):
        # open_in_browser(response)
        mainCat = []
        link = []
        nameList = []
        menu_DF = pd.DataFrame(columns= ['Category', 'Sub Category', 'name'])
        
        menu = response.xpath('//div[@id="menu_sitemap_container"]/ul/li')
        for index in menu:
            mainCat.append(index.css('span::text').extract())
        
        menu = response.css('div#menu_sitemap_container ul li ul')
        for index in menu:
            nameList.append(index.xpath('li/a/text()').extract())
            link.append(index.xpath('li/a/@href').extract())
                
        for index in nameList:
            if len(index)== 0:
                nameList.remove(index)
                link.remove(index)
        # print('NOS: ', nameList)
        j = 0
        for cat in mainCat:
            category = cat[0]
            if len(cat) > 1:
                for i in range(0,len(cat)-1):
                    subcategory = cat[i+1]
                    inameList = nameList[i+j]
                    linkList = link[i+j]
                    for item, li in zip(inameList, linkList):
                        iname = item
                        yield response.follow(li, callback= self.get_nutritional, cb_kwargs= {'category': category, 'subcategory': subcategory, 'iname': iname})
                        menu_DF = menu_DF.append({'Category': category, 'Sub Category': subcategory, 'name': iname}, ignore_index= True)
                j = j + len(cat) -1

            else:
                subcategory = ""
                inameList = nameList[j]
                linkList = link[j]
                for item, li in zip(inameList, linkList):
                    iname = item
                    yield response.follow(li, callback= self.get_nutritional, cb_kwargs= {'category': category, 'subcategory': subcategory, 'iname': iname})
                    menu_DF = menu_DF.append({'Category': category, 'Sub Category': subcategory, 'name': iname}, ignore_index= True)
                    
                j = j + len(cat)
                
        #menu_DF.to_csv('Carljr.csv', encoding= 'utf8', index= False)

    def get_nutritional(self, response, category, subcategory, iname):
        
        self.driver.get(response.url)
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, 'cal_main_right_hero_img')))
        #time.sleep(3)
        scrapy_selector = Selector(text= self.driver.page_source)
        
        desc = scrapy_selector.css('h2#cal_main_right_subtitle::text').get()
        allergy = scrapy_selector.css('ul#cal_info_stats_allergenslist li::text').extract()
        allergy = "".join(allergy)
        nutrition_table = scrapy_selector.xpath('//table[@id= "cal_info_stats_table"]/tbody')
        nutrition_name = nutrition_table.css('th[scope=row]::text').extract()
        nutrition_name = list(map(lambda x: x.strip(), nutrition_name))
        nutrition_value = nutrition_table.css('td[class != mod_col]::text').extract()
        dictOfnutrition = dict(zip(nutrition_name, nutrition_value))
        # print('NOS: ', allergy)

        self.desc_DF = self.desc_DF.append({'Category': category, 'Sub Category': subcategory, 'Name': iname, 'Description': desc,
                                             'Nutritional value': dictOfnutrition, 'Allergens': allergy}, ignore_index= True)

        self.desc_DF.to_csv('Carljr_Website.csv', encoding= 'utf8', index= False)