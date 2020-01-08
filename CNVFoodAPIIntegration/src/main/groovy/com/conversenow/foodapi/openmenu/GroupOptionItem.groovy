package com.conversenow.foodapi.openmenu

class GroupOptionItem {
    def menu_group_option_name, menu_group_option_additional_cost, selected

    GroupOptionItem(){}
    GroupOptionItem(item){
        this.menu_group_option_additional_cost = item.menu_group_option_additional_cost
        this.menu_group_option_name = item.menu_group_option_name
        this.selected = item.selected
    }
}
