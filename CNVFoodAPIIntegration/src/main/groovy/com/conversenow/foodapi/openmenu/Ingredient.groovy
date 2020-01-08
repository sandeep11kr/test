package com.conversenow.foodapi.openmenu

class Ingredient {
    def ingredient_id = '', description = '', manufacturer = '', food_group = '', refuse_percentage = '', refuse_description = '', weight_in_grams = ''
    List<Measurement> measurements
    def calories
    List<Nutrition> nutritions = new ArrayList<>()
    def claims
    protected Ingredient(){}

    Ingredient(ingredient_info){
        this.ingredient_id = ingredient_info.ingredient_id
        this.description = ingredient_info.description
        this.manufacturer = ingredient_info.manufacturer
        this.food_group = ingredient_info.food_group
        this.refuse_percentage = ingredient_info.refuse_percentage
        this.refuse_description = ingredient_info.refuse_description
        this.weight_in_grams = ingredient_info.weight_in_grams
        this.buildCalories(ingredient_info.calories)
        this.buildClaims(ingredient_info.claims)
        this.buildMeasurements(ingredient_info.measurements)
        this.buildNutrition(ingredient_info.nutrition)
    }
    def buildMeasurements(measurement){
        this.measurements = measurement.collect{
            new Measurement(it.value)
        }
    }
    def buildCalories(calories){
        this.calories = new Calories(calories)
    }
    def buildNutrition(nutritionInfos){
        nutritionInfos.each{
            this.nutritions.add(new Nutrition(it))
        }
    }
    def buildClaims(claims){
        this.claims = new Claims(claims)
    }

    @Override
    public String toString() {
        return "Ingredient{" +
                "ingredient_id=" + ingredient_id +
                ", description=" + description +
                ", manufacturer=" + manufacturer +
                ", food_group=" + food_group +
                ", refuse_percentage=" + refuse_percentage +
                ", refuse_description=" + refuse_description +
                ", weight_in_grams=" + weight_in_grams +
                ", measurements=" + measurements +
                ", calories=" + calories +
                ", nutrition=" + nutrition +
                ", claims=" + claims +
                '}';
    }
}
