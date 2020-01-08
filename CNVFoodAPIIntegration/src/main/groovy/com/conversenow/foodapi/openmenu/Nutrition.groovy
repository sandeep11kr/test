package com.conversenow.foodapi.openmenu

class Nutrition {
    def name = '', amount = '', units = '', daily_value = ''

    protected Nutrition(){}
    Nutrition(nutrition){
        this.name = nutrition.key
        this.amount = nutrition?.value.amount
        this.units = nutrition?.value.units
        this.daily_value = nutrition?.value.daily_value
    }
}
