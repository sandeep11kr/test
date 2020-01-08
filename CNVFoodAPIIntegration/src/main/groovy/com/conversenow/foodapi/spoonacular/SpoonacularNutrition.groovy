package com.conversenow.foodapi.spoonacular

import com.conversenow.foodapi.openmenu.Nutrition

class SpoonacularNutrition extends Nutrition{

    SpoonacularNutrition(nutrition) {
        this.name = nutrition.title
        this.amount = nutrition.amount
        this.units = nutrition.unit
        this.daily_value = nutrition.percentOfDailyNeeds
    }
}
