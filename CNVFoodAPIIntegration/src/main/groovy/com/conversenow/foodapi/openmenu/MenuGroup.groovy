package com.conversenow.foodapi.openmenu

class MenuGroup {
    def group_name, group_description
    def menu_items = new ArrayList()
    def group_options = new ArrayList()

    MenuGroup(group_info){
        this.group_name = group_info.group_name
        this.group_description = group_info.group_description
        this.buildMenuItems(group_info.menu_items)
        this.buildGroupOptions(group_info.menu_group_options)
    }
    def buildGroupOptions(options){
        options.forEach{
            this.group_options.add(new GroupOptions(it))
        }
        if(this.group_options.isEmpty()){
            this.group_options.add(new GroupOptions())
        }
    }
    def buildMenuItems(items){
        items.each {
            this.menu_items.add(new MenuItem(it))
        }
    }


    @Override
    public String toString() {
        return "MenuGroup{" +
                "group_name=" + group_name +
                ", group_description=" + group_description +
                ", menu_items=" + menu_items +
                '}';
    }
}
