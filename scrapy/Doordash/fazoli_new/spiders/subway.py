# -*- coding: utf-8 -*-
import scrapy
import json
import re
import pandas as pd



class SubwaySpider(scrapy.Spider):
    name = 'subway'
    allowed_domains = ['doordash.com']
    start_urls = ['https://api-consumer-client.doordash.com/graphql']
    address = ""
    storeTiming = ""

    s_DF = pd.DataFrame()   # DataFrame for ['ID', 'Suggested Item']
    fazoli_DF = pd.DataFrame()  # DataFrame for ['ID', 'Category', 'Name', 'Description', 'Price', 'Calories']

    def start_requests(self):
        params = {"operationName":"menu","variables":{"storeId":"292254","ddffWebHomepageCmsBanner":True},"query":"query menu($storeId: ID!, $menuId: ID, $ddffWebHomepageCmsBanner: Boolean) {\n  storeInformation(storeId: $storeId) {\n    id\n    name\n    description\n    isGoodForGroupOrders\n    offersPickup\n    offersDelivery\n    deliveryFee\n    sosDeliveryFee\n    numRatings\n    averageRating\n    shouldShowStoreLogo\n    isConsumerSubscriptionEligible\n    headerImgUrl\n    coverImgUrl\n    distanceFromConsumer\n    distanceFromConsumerInMeters\n    providesExternalCourierTracking\n    fulfillsOwnDeliveries\n    isInDemandTest\n    isDeliverableToConsumerAddress\n    priceRange\n    business {\n      id\n      name\n      __typename\n    }\n    address {\n      street\n      printableAddress\n      lat\n      lng\n      city\n      state\n      country\n      __typename\n    }\n    status {\n      asapAvailable\n      scheduledAvailable\n      asapMinutesRange\n      asapPickupMinutesRange\n      __typename\n    }\n    merchantPromotions {\n      id\n      minimumOrderCartSubtotal\n      newStoreCustomersOnly\n      deliveryFee\n      categoryId\n      __typename\n    }\n    storeDisclaimers {\n      id\n      disclaimerDetailsLink\n      disclaimerLinkSubstring\n      disclaimerText\n      displayTreatment\n      __typename\n    }\n    __typename\n  }\n  storeMenus(storeId: $storeId, menuId: $menuId) {\n    allMenus {\n      id\n      name\n      subtitle\n      isBusinessEnabled\n      timesOpen\n      __typename\n    }\n    currentMenu {\n      id\n      timesOpen\n      hoursToOrderInAdvance\n      isCatering\n      minOrderSize\n      menuCategories {\n        ...StoreMenuCategoryFragment\n        items {\n          ...StoreMenuListItemFragment\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  storeCrossLinks(storeId: $storeId) {\n    trendingStores {\n      ...StoreCrossLinkItemFragment\n      __typename\n    }\n    trendingCategories {\n      ...StoreCrossLinkItemFragment\n      __typename\n    }\n    topCuisinesNearMe {\n      ...StoreCrossLinkItemFragment\n      __typename\n    }\n    nearbyCities {\n      ...StoreCrossLinkItemFragment\n      __typename\n    }\n    __typename\n  }\n  storeMenuSeo(storeId: $storeId, menuId: $menuId)\n  consumerAllMarketingMessages(ddffWebHomepageCmsBanner: $ddffWebHomepageCmsBanner) {\n    ...MenuConsumerAllMarketingMessageFragment\n    __typename\n  }\n  consumerCmsDetails(placement: \"store\", storeId: $storeId, ddffWebHomepageCmsBanner: $ddffWebHomepageCmsBanner) {\n    banner {\n      isActive\n      description {\n        copy\n        color\n        __typename\n      }\n      modal {\n        description\n        label\n        terms\n        __typename\n      }\n      url\n      backgroundColor\n      desktopImage\n      mobileImage\n      opensModal\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment StoreMenuCategoryFragment on StoreMenuCategory {\n  id\n  subtitle\n  title\n  __typename\n}\n\nfragment StoreMenuListItemFragment on StoreMenuListItem {\n  id\n  description\n  isTempDeactivated\n  price\n  imageUrl\n  name\n  __typename\n}\n\nfragment StoreCrossLinkItemFragment on StoreCrossLinkItem {\n  name\n  url\n  __typename\n}\n\nfragment MenuConsumerAllMarketingMessageFragment on MarketingMessage {\n  featuredLocationInfo {\n    description\n    title\n    __typename\n  }\n  type\n  __typename\n}\n"}
        header = {"Content-Type": "application/json"}
        cookies = {"Cookie": "csrf_token=tlCsTGHJLq0xFoppweYuqpWBFdcegEgX2MBj614mLuK6O4VYhGIssXDRT3WAt9S3; dd_session_id_2=sx_b83058d5e260494a93aab1b7c5f4a327; dd_guest_id=fc6f6461-f082-4633-90b6-88fd2ed4a08e; dd_session_id=sx_1bc677d0044c43d996fffd4d59f7d15f; dd_device_id=dx_2392510f150b4a7081944d118f62e642; dd_login_id=lx_7511091ec515426a974d4aaa9049ba1a; dd_device_id_2=dx_fb01dbfefb414140a59ff4ef6c868805; doordash_attempt_canary=0; ajs_user_id=null; ajs_group_id=null; ajs_anonymous_id=%22ad0b7dfd-0b6a-4eb6-8615-3e18245aa3d2%22; _gcl_au=1.1.409857846.1574503717; _dpm_ses.4dc2=*; _dpm_id.4dc2=a358b677-d91a-46b7-891b-3e0fcc4fb3b5.1574503724.1.1574503724.1574503724.66c33790-0dfa-495a-b474-f887bd860a3a"}

        for url in self.start_urls:
            yield scrapy.Request(url= url, callback= self.parse, method= 'POST', headers= header, body= json.dumps(params), cookies= cookies)

    def parse(self, response):
        #open_in_browser(response)
        dataList = []
        calorie = ""
        content = response.body
        content = json.loads(content)
        menuCategories = content['data']['storeMenus']['currentMenu']['menuCategories']
        for allItems in menuCategories:
            title = allItems['title']
            items = allItems['items']
            for item in items:
                itemId = int(item['id'])
                iname = item['name']
                desc = item['description']
                prices = item['price']
                prices = prices/100
                # filtering calorie column and removing same from desc coloumn
                if re.search(r"\d{2,}[/|-]\d{2,}", desc):
                    calorie = re.search(r"\d{2,}[/|-]\d{2,}", desc).group()
                    desc = re.sub(calorie,'',desc)
                elif re.search(r"\d{2,}", desc):
                    calorie = re.search(r"\d{2,}", desc).group()
                    desc = re.sub(calorie,'',desc)
                else:
                    calorie = ""
                desc = re.sub(r'cal.',"", desc)
                 
                tup1 = (itemId, title, iname, desc, prices, calorie)
                dataList.append(tup1)
            
        self.address = content['data']['storeInformation']['address']['printableAddress']
        self.address = re.sub(r',', " ",self.address)
        self.storeTiming = content['data']['storeMenus']['currentMenu']['timesOpen'][0]
        self.fazoli_DF = pd.DataFrame(data= dataList, columns= ['ID', 'Category', 'Name', 'Description', 'Price', 'Calories'])
                
        with open('Subway_DoorDash.csv', 'w', newline= '\n', encoding= 'utf8') as f:
            f.write(self.address+'\n')
            f.write('Timing: '+self.storeTiming+'\n\n')
            self.fazoli_DF.to_csv(f, index= False, header= True)
        
        params1 = {"operationName":"menuItem","variables":{"storeId":"292254","itemId":104427889},"query":"query menuItem($storeId: ID!, $itemId: ID!, $optionId: ID, $optionDbId: ID) {\n  menuItem(storeId: $storeId, itemId: $itemId, optionId: $optionId, optionDbId: $optionDbId) {\n    item {\n      description\n      price\n      minAgeRequirement\n      id\n      name\n      imageUrl\n      extras\n      specialInstructionsMaxLength\n      priceMonetaryFields {\n        ...ItemPriceMonetaryFieldsFragment\n        __typename\n      }\n      __typename\n    }\n    extras {\n      ...ItemExtraFragment\n      __typename\n    }\n    options {\n      ...ItemOptionFragment\n      __typename\n    }\n    suggestedItems {\n      ...SuggestedItemFragment\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment ItemPriceMonetaryFieldsFragment on ItemPriceMonetaryFields {\n  displayString\n  unitAmount\n  __typename\n}\n\nfragment ItemExtraFragment on ItemExtra {\n  id\n  dbId\n  parentOptionId\n  selectionMode\n  maxNumOptions\n  description\n  minAggregateOptionsQuantity\n  maxOptionChoiceQuantity\n  isActive\n  minOptionChoiceQuantity\n  maxAggregateOptionsQuantity\n  minNumOptions\n  numFreeOptions\n  name\n  options\n  defaultItemExtraOptions\n  __typename\n}\n\nfragment ItemOptionFragment on ItemOption {\n  id\n  dbId\n  parentExtraId\n  description\n  price\n  numExtras\n  name\n  extras\n  priceMonetaryFields {\n    ...ItemPriceMonetaryFieldsFragment\n    __typename\n  }\n  __typename\n}\n\nfragment SuggestedItemFragment on SuggestedItem {\n  id\n  name\n  merchantSuppliedId\n  description\n  price\n  minAgeRequirement\n  isActive\n  deactivation\n  menuItemNumber\n  basePrice\n  category {\n    subtitle\n    name\n    title\n    isActive\n    sortId\n    merchantSuppliedId\n    id\n    __typename\n  }\n  priceMonetaryFields {\n    ...ItemPriceMonetaryFieldsFragment\n    __typename\n  }\n  __typename\n}\n"}
        header1 = {"Content-Type": "application/json"}
        cookies1 = {"Cookie": "csrf_token=jn01KB1NQqInQwFuDKJBDl4NpIcwK3EY5gvJ2aUERrSmYojAPYN4hgq5GxlDyHIy; dd_session_id_2=sx_9aa90ce0021b401792383fcfa94926ba; dd_guest_id=2e15c710-7dd2-4f83-9df3-00e135dddefa; dd_session_id=sx_6a831ba83b6e42738b646518318d1d69; dd_device_id=dx_e02cb4462cf0423ea0236a88cf369bdb; dd_login_id=lx_957eb100484946729ac4148b32175c86; dd_device_id_2=dx_106185949b424a82a6efbedba67423c1; doordash_attempt_canary=0; ajs_user_id=null; ajs_group_id=null; ajs_anonymous_id=%22d42832b0-f3f6-45b7-b998-89e0682783b5%22; _gcl_au=1.1.7190899.1574744360; _dpm_ses.4dc2=*; _dpm_id.4dc2=bc983d54-f51d-4086-8884-f4c45c8a7a06.1574744361.1.1574744376.1574744361.810ea329-2573-4f02-a355-f36298e4a8f3; dd_submarket_id=38; dd_district_id=1488; dd_zip_code=78729"}
        for id in self.fazoli_DF['ID']:
            params1['variables']['itemId']= id
            yield response.follow(url= response.url, callback= self.recom_method, method= 'POST', headers= header1, body= json.dumps(params1), cookies= cookies1)

                    

    def recom_method(self, response):
       
        sItemList = [] #List of suggested Item
        content = response.body
        content = json.loads(content)
        #iname = content['data']['menuItem']['item']['name']
        itemId = int(content['data']['menuItem']['item']['id'])
        suggestedCategories = content['data']['menuItem']['suggestedItems']
        for index in suggestedCategories:
            suggestItem = index['name']
            sItemList.append(suggestItem)
        self.s_DF = self.s_DF.append({'ID': itemId, 'Suggested Item': sItemList}, ignore_index= True)
        mergeDF = self.fazoli_DF.merge(self.s_DF, how='left')
        fun1 = lambda a: '/'.join(a)  # merging Category of dublicate 'Name' column in one
        fun2 = lambda a: list(a)[0]   # Nothing to do with other columns
        groupbyCatDF = mergeDF.groupby('Name').agg({
                'ID': fun2,
                'Category': fun1,
                'Description': fun2,
                'Price': fun2,
                'Calories': fun2,
                'Suggested Item': fun2,
        }).reset_index()
        
        zip = self.address.split()[-2]
        
        with open('Subway_DoorDash_Austin_{}.csv'.format(zip), 'w', newline= '\n', encoding= 'utf8') as f:
            f.write(self.address+'\n')
            f.write('Timing: '+self.storeTiming+'\n\n')
            groupbyCatDF.to_csv(f, index= False)
    