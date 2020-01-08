import json
import configparser
import pyorient

class MenuItems:
	config = configparser.ConfigParser()
	config.read('config/config.ini')

	def __init__(self):
		self.db = self.config['DEFAULT']['db']
		self.db_user = self.config['DEFAULT']['db_user']
		self.db_password = self.config['DEFAULT']['db_password']

	def saveMenuItems(self):
		orientclient = pyorient.OrientDB("localhost", 2424)
		orientclient.db_open(self.db, self.db_user, self.db_password)
		menuFile = self.config['DEFAULT']['menu']
		with open(menuFile) as json_file:
			data = json.load(json_file)
			self.storeInDB(orientclient, data)
		orientclient.db_close()

	def storeInDB(self, orientclient, data):
		dbData = {}
		orientclient.db_open(self.db, self.db_user, self.db_password)
		for menu in data:
			dbData['@MenuItem']=menu
			self.storeRecord(orientclient, dbData)

	def storeRecord(self, orientclient, data):
		print(data)
		orientclient.record_create(-1, data)

	def loadMenuItemWithId(self, itemid, orientclient):
		items = orientclient.query("Select from MenuItem where id=" + itemid)
		menuItem = {}
		for item in items:
			menuItem = item
		return menuItem



