package com.conversenow.foodapi.openmenu

import groovy.json.JsonSlurper

class JsonLoader {
    def jsonSlurper = new JsonSlurper()
    def load(filePath){
        jsonSlurper.parse(new File(filePath))
    }
}
