import json
import configparser
import pyorient
from data.menuitems.menuitems import MenuItems

class Store:
    config = configparser.ConfigParser()
    config.read('../config/config.ini')

    def getStoreMenuItems(self, recommendations, orientclient):
        menuitems = MenuItems()
        items = []
        for recommendation in recommendations:
            item = menuitems.loadMenuItemWithId(str(recommendation['master_product_id']),orientclient)
            items.append( pyorient.OrientRecordLink(item._rid))
        return items

    # select menuitems from Store where name like "Fazoli's" and zipcode=78727
    def findAllMenuItemsForStore(self,name, zipcode):
        client = pyorient.OrientDB("localhost", 2424)
        client.db_open("conversenow", "root", "root")
        query = 'select from Store where name like "' + name + '" and zipcode like "' + str(zipcode) + '"'
        itemrecs = client.query(query)
        menuitems = []
        for item in itemrecs[0].menuitems:
            menuitems.append(client.record_load(item))
        client.db_close()
        return menuitems

    # select menuitems from Store where name like "Fazoli's" and zipcode=78727
    def findAllStores(self):
        client = pyorient.OrientDB("localhost", 2424)
        client.db_open("conversenow", "root", "root")
        query = 'select from Store'
        stores = client.query(query)
        client.db_close()
        return stores

    # Select From MenuItem where @rid in 
    # (Select recommendeditems From RecommendationCluster 
    # where @rid in (Select recommendations['16234863'] from Store))
    def findAllRecommendationsForItem(self, selectedItem, zipcode):
        client = pyorient.OrientDB("localhost", 2424)
        client.db_open("conversenow", "root", "root")
        query = """select expand(in) from 
            (select expand(recommendations['{}'].recommendeditems) 
            as items from Store 
            where zipcode like '{}')""".\
            format(selectedItem,zipcode)
        print(query)
        itemrecs = client.query(query)
        print(itemrecs)
        menuitems = []
        for item in itemrecs:
            menuitems.append(item)
        print("Recommending")
        for item in menuitems:
            print(item.name)
        client.db_close()
        return menuitems
