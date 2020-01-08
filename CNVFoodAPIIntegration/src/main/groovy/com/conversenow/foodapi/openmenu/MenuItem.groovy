package com.conversenow.foodapi.openmenu

class MenuItem {
    def menu_item_name, menu_item_description, menu_item_price, menu_item_calories, menu_item_heat_index, vegetarian, vegan
    def menu_item_allergy_information, menu_item_allergy_information_allergens, special, halal, kosher, gluten_free

    MenuItem(item){
        this.menu_item_name = item.menu_item_name
        this.menu_item_description = item.menu_item_description
        this.menu_item_price = item.menu_item_price
        this.menu_item_calories = item.menu_item_calories
        this.vegetarian = item.vegetarian
        this.vegan = item.vegan
        this.menu_item_heat_index = item.menu_item_heat_index
        this.menu_item_allergy_information = item.menu_item_allergy_information
        this.menu_item_allergy_information_allergens = item.menu_item_allergy_information_allergens
        this.special = item.special
        this.halal = item.halal
        this.kosher = item.kosher
        this.gluten_free = item.gluten_free
    }


    @Override
    public String toString() {
        return "MenuItem{" +
                "menu_item_name=" + menu_item_name +
                ", menu_item_description=" + menu_item_description +
                ", menu_item_price=" + menu_item_price +
                ", menu_item_calories=" + menu_item_calories +
                ", vegetarian=" + vegetarian +
                ", vegan=" + vegan +
                '}';
    }
}
