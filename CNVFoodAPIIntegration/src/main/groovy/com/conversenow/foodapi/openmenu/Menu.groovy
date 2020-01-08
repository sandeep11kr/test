package com.conversenow.foodapi.openmenu

class Menu {
    def menu_name, menu_description, menu_duration_name, menu_duration_time_start, menu_duration_time_end
    def menu_groups= new ArrayList()

    Menu(menu_info){
        this.menu_name = menu_info.menu_name
        this.menu_description = menu_info.menu_description
        this.menu_duration_name = menu_info.menu_duration_name
        this.menu_duration_time_start = menu_info.menu_duration_time_start
        this.menu_duration_time_end = menu_info.menu_duration_time_end
        buildMenuGroups(menu_info.menu_groups)
    }

    def buildMenuGroups(groups){
       groups.each {
           this.menu_groups.add(new MenuGroup((it)))
       }
    }


    @Override
    public String toString() {
        return "Menu{" +
                "menu_name=" + menu_name +
                ", menu_description=" + menu_description +
                ", menu_duration_name=" + menu_duration_name +
                ", menu_duration_time_start=" + menu_duration_time_start +
                ", menu_duration_time_end=" + menu_duration_time_end +
                ", menu_groups=" + menu_groups +
                '}';
    }
}
