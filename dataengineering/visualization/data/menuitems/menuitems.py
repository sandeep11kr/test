import json
import configparser
import pyorient

class MenuItems:
	config = configparser.ConfigParser()
	config.read('../config/config.ini')

	def loadMenuItemWithId(self, itemid, orientclient):
		items = orientclient.query("Select from MenuItem where id=" + itemid)
		menuItem = {}
		for item in items:
			menuItem = item
		return menuItem

	def findAllMenuCategoriesInStore(self, storeid):
		client = pyorient.OrientDB("localhost", 2424)
		client.db_open("conversenow", "root", "root")
		query = "select distinct(category) as category from MenuItem"
		records = client.query(query)
		categories = []
		for record in records:
			categories.append(record.category)
		client.db_close()
		return categories




