package com.conversenow.foodapi.openmenu

class Restaurant {
    String id, restaurant_name, brief_description, address_1, address_2, city_town, state_province, postal_code, country
    def menus = new ArrayList()

    Restaurant(restaurant_info, menus = null){
        this.id = restaurant_info.id
        this.restaurant_name = restaurant_info.restaurant_name
        this.brief_description = restaurant_info.brief_description
        this.address_1 = restaurant_info.address_1
        this.address_2 = restaurant_info.address_2
        this.city_town = restaurant_info.city_town
        this.state_province = restaurant_info.state_province
        this.postal_code = restaurant_info.postal_code
        this.country = restaurant_info.country
        if(menus!=null)
            this.buildMenu(menus)
    }

    def buildMenu(restaurantMenus){
        restaurantMenus.each {
            this.menus.add(new Menu(it))
        }
    }

    @Override
    String toString() {
        return "Restaurant{" +
                "restaurant_name=" + restaurant_name +
                ", brief_description=" + brief_description +
                ", address_1=" + address_1 +
                ", address_2=" + address_2 +
                ", city_town=" + city_town +
                ", state_province=" + state_province +
                ", postal_code=" + postal_code +
                ", country=" + country +
                ", menus=" + menus +
                '}';
    }
}
