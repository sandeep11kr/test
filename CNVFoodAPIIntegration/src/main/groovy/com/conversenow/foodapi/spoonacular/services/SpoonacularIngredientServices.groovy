package com.conversenow.foodapi.spoonacular.services

import com.conversenow.foodapi.openmenu.Ingredient
import com.conversenow.foodapi.openmenu.Log
import com.conversenow.foodapi.spoonacular.SpoonacularIngredients
import groovyx.net.http.RESTClient
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.beans.factory.annotation.Value
import org.springframework.stereotype.Service

import javax.annotation.PostConstruct

@Service
class SpoonacularIngredientServices {
    @Autowired Log log
    @Value('${spoonacular_key}') String api_key
    def openmenu = null

    @PostConstruct
    def initClass(){
        openmenu = new RESTClient( "https://api.spoonacular.com/recipes/parseIngredients?apiKey=$api_key" )
    }
    def loadIngredientDetails(String foodItem){
        log.addLog("Loading ingredients for $foodItem")
        try{
            def result = openmenu.post(
                    contentType:'application/json',
                    requestContentType: 'application/x-www-form-urlencoded',
                    body:[ingredientList:foodItem, includeNutrition:true]
            )
            def ingredients = result.data
            log.addLog("Loaded ${ingredients?.size()} ingredient details")
            ingredients.collect{
                new SpoonacularIngredients(it)
            }
        }catch(Exception e){
            this.log.addLog("Unable to load ingredients ${e.getLocalizedMessage()}")
            throw e
        }
    }
}
