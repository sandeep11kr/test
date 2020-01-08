package com.conversenow.foodapi.openmenu

class Measurement {
    def description, weight_amount, weight_grams, edible_portion

    Measurement(measurement){
        this.description = measurement?.description
        this.weight_amount = measurement?.weight_amount
        this.weight_grams = measurement?.weight_grams
        this.edible_portion = measurement?.edible_portion
    }
}
