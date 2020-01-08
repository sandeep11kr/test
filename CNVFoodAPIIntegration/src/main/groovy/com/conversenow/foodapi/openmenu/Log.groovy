package com.conversenow.foodapi.openmenu

import org.springframework.stereotype.Service

import java.text.SimpleDateFormat
import java.time.Instant
import java.time.LocalDateTime
import java.time.ZoneId

@Service
class Log {
    def addLog(text){
        def dateFormatter = new SimpleDateFormat('yyyy-MM-dd hh:mm:ss')
        def currTimeInMillis = System.currentTimeMillis()
        def timeInMillis = milliToDate(currTimeInMillis)
        def formattedDate = dateFormatter.format(new Date(currTimeInMillis))

        println "$formattedDate  $text"
    }
    static milliToDate(millis){
        LocalDateTime.ofInstant(Instant.ofEpochMilli(millis), ZoneId.of('Asia/Kolkata'))
    }
}
