package com.conversenow.foodapi.openmenu.services

import com.conversenow.foodapi.openmenu.Log
import com.conversenow.foodapi.openmenu.Restaurant
import groovyx.net.http.RESTClient
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.beans.factory.annotation.Value
import org.springframework.stereotype.Service

import javax.annotation.PostConstruct

@Service
class OpenMenuMenuServices {
    @Autowired Log log
    @Value('${openmenu_key}') String api_key
    def openmenu = null

    @PostConstruct
    def initClass(){
        openmenu = new RESTClient( 'https://openmenu.com/api/v2/restaurant.php' )
    }
    def loadRestaurantMenu(String restaurantId){
        log.addLog("Loading menu details for restaurant with id $restaurantId")
        def result = openmenu.get(query:['key': api_key,'id': restaurantId])
        def restaurantDetails = result.data.response.result.restaurant_info
        def menus = result.data.response.result.menus
        log.addLog("Loaded ${menus?.size()} menu details")
        new Restaurant(restaurantDetails, menus)
    }
}
