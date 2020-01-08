package com.conversenow.foodapi.openmenu.services

import com.conversenow.foodapi.openmenu.Log
import com.conversenow.foodapi.openmenu.Restaurant
import groovyx.net.http.RESTClient
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.beans.factory.annotation.Value
import org.springframework.stereotype.Service

import javax.annotation.PostConstruct

@Service
class OpenMenuRestaurantServices {
    @Autowired Log log
    @Value('${openmenu_key}') String api_key
    def openmenu = null

    @PostConstruct
    def initClass(){
        openmenu = new RESTClient( 'https://openmenu.com/api/v2/location.php' )
    }
    def loadAtLocation(String name, String postal_code,String city){
        def queryMap = ['key': api_key, 'country': 'US', 's': name]
        if(postal_code!=null)
            queryMap.put('postal_code', postal_code)
        if(city!=null)
            queryMap.put('city', city)
        def result = openmenu.get(query:queryMap)
        def restaurants = result.data.response.result.restaurants
        log.addLog("Loading restaurants named $name at $postal_code")
        restaurants = loadRestaurants(restaurants).findAll {
            if(name != null && name.trim().length()>0) {
                it.restaurant_name.toLowerCase().contains(name.toLowerCase())
            }else{
                it
            }
        }
        log.addLog("Loaded ${restaurants?.size()} restaurants")
        restaurants
    }

    private def loadRestaurants(data){
        data.collect {
            new Restaurant(it)
        }
    }
}
