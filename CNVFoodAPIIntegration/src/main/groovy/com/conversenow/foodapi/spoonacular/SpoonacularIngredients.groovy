package com.conversenow.foodapi.spoonacular

import com.conversenow.foodapi.openmenu.Ingredient
import com.conversenow.foodapi.openmenu.Nutrition


class SpoonacularIngredients extends Ingredient{

    SpoonacularIngredients(ingredient_info) {
        this.ingredient_id = ingredient_info.id
        this.description = ingredient_info.originalName
        this.manufacturer = ''
        this.food_group = ingredient_info.aisle
        this.refuse_percentage = ''
        this.refuse_description = ''
        this.weight_in_grams = ''
        this.buildCalories(
                getNutritionObject(ingredient_info.nutrition.nutrients, 'Calories'),
                ingredient_info.nutrition.caloricBreakdown
        )
        this.buildMeasurements(ingredient_info.measurements)
        this.buildNutrition(ingredient_info.nutrition.nutrients)
    }
    def getNutritionObject(nutritionInfos, title){
        nutritionInfos.find {
            it.title==title
        }
    }
    def buildCalories(cal, calorificBreakdown){
        this.calories = new SpoonacularCalories(cal, calorificBreakdown)
    }
    def buildNutrition(nutritionInfo){
        nutritionInfo.each {
            this.nutritions.add(new SpoonacularNutrition(it))
        }
    }
}
