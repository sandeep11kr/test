package com.conversenow.foodapi.openmenu

class Claims {
    def alcohol_free = '', sodium_free = '', good_source_protein = '', high_protein = '', good_source_fiber = '', high_fiber = ''

    Claims(claims){
        this.alcohol_free = claims?.alcohol_free
        this.sodium_free = claims?.sodium_free
        this.good_source_protein = claims?.good_source_protein
        this.high_protein = claims?.high_protein
        this.good_source_fiber = claims?.good_source_fiber
        this.high_fiber = claims?.high_fiber
    }
}
