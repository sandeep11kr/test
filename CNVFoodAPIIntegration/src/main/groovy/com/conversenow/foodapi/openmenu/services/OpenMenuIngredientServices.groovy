package com.conversenow.foodapi.openmenu.services

import com.conversenow.foodapi.openmenu.Ingredient
import com.conversenow.foodapi.openmenu.Log
import groovyx.net.http.RESTClient
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.beans.factory.annotation.Value
import org.springframework.stereotype.Service

import javax.annotation.PostConstruct

@Service
class OpenMenuIngredientServices {
    @Autowired Log log
    @Value('${openmenu_key}') String api_key
    def openmenu = null

    @PostConstruct
    def initClass(){
        openmenu = new RESTClient( 'https://openmenu.com/api/v2/ingredients.php' )
    }
    def loadIngredientDetails(String foodItem){
        log.addLog("Loading ingredients for $foodItem")
        def result = openmenu.get(query:['key': api_key,'s': foodItem,'nutrition':1])
        def ingredients = result.data.response.result.ingredients
        log.addLog("Loaded ${ingredients?.size()} ingredient details")
        ingredients.collect{
            new Ingredient(it)
        }
    }
}
