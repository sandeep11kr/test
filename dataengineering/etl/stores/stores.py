import json
import configparser
import pyorient
from menuitems.menuitems import MenuItems

class Store:
    config = configparser.ConfigParser()
    config.read('config/config.ini')

    def __init__(self):
        self.db = self.config['DEFAULT']['db']
        self.db_user = self.config['DEFAULT']['db_user']
        self.db_password = self.config['DEFAULT']['db_password']

    def saveStores(self):
        orientclient = pyorient.OrientDB("localhost", 2424)
        orientclient.db_open(self.db, self.db_user, self.db_password)
        storeFile = self.config['DEFAULT']['stores']
        with open(storeFile) as json_file:
            data = json.load(json_file)
            self.saveStoreDetails(data, orientclient)
        orientclient.db_close()

    #"store": {
    #  "name": "Fazoli's",
    #  "address": "Fazoli's  13201 Ranch Road 620 N Suite S  Austin  TX 78727",
    #  "zipcode": 78727
    #},
    #"recommendations": [        
    def saveStoreDetails(self, storeData, orientclient):
        print("Storing recommendations ")
        storeRecommendationSet = storeData['recommendations']
        recommendations = self.storeRecommendations(storeRecommendationSet, orientclient)
        storeData['store']['recommendations'] = recommendations
        storeData['store']['menuitems'] = self.getStoreMenuItems(storeRecommendationSet, orientclient)
        dbData = {}
        print("Storing Store Data")        
        dbData['@Store']=storeData['store']
        orientclient.record_create(-1, dbData)
        print("Created store")

    def getStoreMenuItems(self, recommendations, orientclient):
        menuitems = MenuItems()
        items = []
        for recommendation in recommendations:
            item = menuitems.loadMenuItemWithId(str(recommendation['master_product_id']),orientclient)
            items.append( pyorient.OrientRecordLink(item._rid))
        return items

    def storeRecommendations(self, recommendations, orientclient):
        recommendationForStore = {}
        print("Storing recommendation clusters ")
        for recommendation in recommendations:
            newCluster = self.storeRecommendationClusters(recommendation, orientclient)
            recommendationForStore[str(recommendation['master_product_id'])]= pyorient.OrientRecordLink(newCluster._rid)
        return recommendationForStore

    #{
    #  "index": 0,
    #  "master_product_id": 16236495,
    #  "recommendation": [
    #    16236291,
    #    16246088,
    #    16246088
    #  ]
    #},
    def storeRecommendationClusters(self, recommendationCluster, orientclient):
        menuitems = MenuItems()
        items = []
        cluster = {}
        dbClustorData = {}
        dbClustorData['@RecommendationCluster']=cluster
        newCluster = orientclient.record_create(-1, dbClustorData)
        clusterrid = newCluster._rid
        print("Storing recommendation cluster ")
        for recommendation in recommendationCluster['recommendation']:
            recItem = {}
            dbData = {}
            item = menuitems.loadMenuItemWithId(str(recommendation),orientclient)
            recItem['in'] = pyorient.OrientRecordLink(item._rid)
            recItem['out'] = pyorient.OrientRecordLink(clusterrid)
            dbData['@RecommendedItem'] = recItem
            newRecItem = orientclient.record_create(-1, dbData)
            items.append(pyorient.OrientRecordLink(newRecItem._rid))  
        recommendeditems = {}
        dbClustorUpdateData = {}
        recommendeditems['recommendeditems'] = items
        dbClustorUpdateData['@RecommendationCluster']= recommendeditems
        print("Updating {} for {} with version {}".format(dbClustorUpdateData, clusterrid, newCluster._version))
        orientclient.record_update(clusterrid, clusterrid, dbClustorUpdateData, newCluster._version)          
        print("Returning new recommendation cluster ")
        return newCluster       

    # select menuitems from Store where name like "Fazoli's" and zipcode=78727
    def findAllMenuItemsForStore(self,name, zipcode):
        client = pyorient.OrientDB("localhost", 2424)
        client.db_open(self.db, self.db_user, self.db_password)
        query = """select from Store where name like {} 
                    and zipcode like {}""".format(name, str(zipcode))
        itemrecs = client.query(query)
        menuitems = []
        for item in itemrecs[0].menuitems:
            menuitems.append(client.record_load(item))
        client.db_close()
        return menuitems

    # Select From MenuItem where @rid in 
    # (Select recommendeditems From RecommendationCluster 
    # where @rid in (Select recommendations['16234863'] from Store))
    def findAllRecommendationsForItem(self, selectedItem):
        client = pyorient.OrientDB("localhost", 2424)
        client.db_open(self.db, self.db_user, self.db_password)
        query = """Select From MenuItem where @rid in 
            (Select recommendeditems From RecommendationCluster 
            where @rid in 
            (Select recommendations[{}] from Store))""".format(str(selectedItem))
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
