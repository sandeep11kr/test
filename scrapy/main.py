import os
from datetime import datetime
import pandas as pd

from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging

from Doordash.fazoli_new.spiders.doordash import DoordashSpider
from Website.Restaurant_Menu.spiders.reData import RedataSpider
from Website.Restaurant_Menu.vpnconfig import VirtualVpn



readPath = os.path.join('Website', 'Fazoli Data', 'Fazoli_Address with url& doorID.xlsx')
url_DF = pd.read_excel(readPath)
url_DF.dropna(inplace=True)
url_DF.reset_index(drop= True, inplace= True)
print(url_DF.index)
idList = url_DF['doordash id']
idList = pd.to_numeric(idList, downcast= 'integer', errors= 'coerce')

date = datetime.now().strftime('%d-%m-%y')
time = datetime.now().strftime('%H-%M')
savePath = os.path.join('cnvfooddrec', 'scrapy', 'fazoli', date, time)
if not os.path.exists(savePath): os.makedirs(savePath)

configure_logging()
runner = CrawlerRunner()
vpn = VirtualVpn()


@defer.inlineCallbacks
def crawl():
    
    #vpn = VirtualVpn()
    for id in idList:                 # This loop for Doordash
        yield runner.crawl(DoordashSpider, id, savePath)    # pass store ID to class as id
    

    for i in range(0, url_DF.shape[0]):            # This loop for website
        url = url_DF.iloc[i, 4]
        city = url_DF.iloc[i, 1]
        pin = url_DF.iloc[i, 3]
        city = city + '_' + str(pin)
        vpn.connect()
        yield runner.crawl(RedataSpider, url, city, savePath)
        vpn.disconnect()
        
           
    reactor.stop()


crawl()
reactor.run()  # the script will block here until the last crawl call is finished

doordash_dir = os.path.join(savePath, 'doordash')
website_dir = os.path.join(savePath, 'website')
if os.path.exists(doordash_dir) and os.path.exists(website_dir):
    with open('scarpy.log', 'w') as f:
        if len(os.listdir(doordash_dir)) == url_DF.shape[0] and len(os.listdir(website_dir)) == url_DF.shape[0]:
            f.write(f'{date} {time} SUCCESS {savePath}')
        else:
            f.write(f'{date} {time} FAILURE {savePath}') 
