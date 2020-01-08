package com.conversenow.foodapi.openmenu

class Calories {
    def calories_alcohol = '', calories_fat = '', calories_carbohydrates = '', calories_protein = '', total = ''

    protected Calories(){}
    Calories(calories){
        this.calories_alcohol = calories?.calories_alcohol
        this.calories_fat = calories?.calories_fat
        this.calories_carbohydrates = calories?.calories_carbohydrates
        this.calories_protein = calories?.calories_protein
        this.total = calories?.total
    }
}
