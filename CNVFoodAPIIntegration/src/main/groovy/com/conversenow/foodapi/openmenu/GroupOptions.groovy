package com.conversenow.foodapi.openmenu

class GroupOptions {
    def name
    def option_items = new ArrayList()

    GroupOptions(option){
        this.name = option.group_options_name
        this.buildOptionItems(option.option_items)
    }
    GroupOptions(){
        this.name = ''
        this.option_items.add(new GroupOptionItem())

    }
    def buildOptionItems(items){
        items.each {
            this.option_items.add(new GroupOptionItem(it))
        }
    }
}
