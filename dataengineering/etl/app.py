import pyorient
from menuitems.menuitems import MenuItems
from stores.stores import Store
menuservice = MenuItems()
menuservice.saveMenuItems()
storesservice = Store()
storesservice.saveStores()


