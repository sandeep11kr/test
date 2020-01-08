package com.conversenow.foodapi.spoonacular

import com.conversenow.foodapi.openmenu.Calories


class SpoonacularCalories extends Calories{
    def percentageOfDailyNeeds
    SpoonacularCalories(calories, breakdown) {
        this.total = calories?.amount
        this.percentageOfDailyNeeds = calories?.percentageOfDailyNeeds
        this.calories_fat = breakdown.percentFat
        this.calories_protein = breakdown.percentProtein
        this.calories_carbohydrates = breakdown.percentCarbs
    }
}
