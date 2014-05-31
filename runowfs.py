#!/usr/bin/env python2.7
print "running..."
import ow
import time
import datetime
import sys # for handling errors
import urllib2 # for sending data to Pachube
import json # for assembling JSON data for Pachube
#import xml.etree.ElementTree as ET # for loading config

#ow.init( 'u' )
    
# We're accessing the 1-wire bus directly from python but
# if you want to use owserver:
ow.init( '-F localhost:3001' ) # /opt/owfs/bin/owserver -p 3030 -u -r

sensors = ow.Sensor('/uncached/1F.3BDE03000000').sensorList()
#sensors = ow.Sensor('/uncached/1F.3BDE03000000').entryList()
# We're only interested in temperature sensors so remove
# any 1-wire devices which aren't temperature sensors
#for sensor in sensors[:]:
#    if sensor.type != 'DS18S20':
#        sensors.remove( sensor )
lastTime = time.time()
lastCount = 0
while True:
    for sensor in sensors[:]:
        #print sensor.entryList(), "\n",
        #print sensor.type
        if sensor.type == 'DS2423':
            windSpeed = sensor
        elif sensor.type == 'DS2450':
            windDir = sensor
        elif sensor.type == 'DS18S20':
            temp = sensor
 

#while True:  
  #  for sensor in sensors:
    currentTime = float(round(time.time() * 1000))
    currentCount = float(windSpeed.counter_A) 
    windSpeed = round(((currentCount-lastCount)/((currentTime-lastTime) / 1000)) / 2 * 2.453, 2)
    #print ws
    #print currentCount-lastCount, currentTime
    print "Windspeed: ", windSpeed, "\t"
    #wd =  int(round(float(windDir.volt_A), 0))
    windList = windDir.volt_ALL.split(",")
    windList = [ round(float(elem),0) for elem in windList ]

    if cmp(windList, [5.0, 5.0, 2.0, 5.0]) == 0 : 
        windDirection = "North"
    elif cmp(windList, [5.0, 3.0, 3.0, 5.0]) == 0 :
        windDirection = "NNE"
    elif cmp(windList, [5.0, 2.0, 5.0, 5.0]) == 0 :
        windDirection = "NE"
    elif cmp(windList, [3.0, 3.0, 5.0, 5.0]) == 0 :
        windDirection = "ENE"
    elif cmp(windList, [2.0, 5.0, 5.0, 5.0]) == 0 :
        windDirection = "East"
    elif cmp(windList, [2.0, 5.0, 5.0, 0.0]) == 0 :
        windDirection = "ESE"
    elif cmp(windList, [5.0, 5.0, 5.0, 0.0]) == 0 :
        windDirection = "SE"
    elif cmp(windList, [5.0, 5.0, 0.0, 0.0]) == 0 :
        windDirection = "SSE"
    elif cmp(windList, [5.0, 5.0, 0.0, 5.0]) == 0 :
        windDirection = "South"
    elif cmp(windList, [5.0, 0.0, 0.0, 5.0]) == 0 :
        windDirection = "SSW"
    elif cmp(windList, [5.0, 0.0, 5.0, 5.0]) == 0 :
        windDirection = "SW"
    elif cmp(windList, [0.0, 0.0, 5.0, 5.0]) == 0 :
        windDirection = "WSW"
    elif cmp(windList, [0.0, 5.0, 5.0, 5.0]) == 0 :
        windDirection = "West"
    elif cmp(windList, [0.0, 5.0, 5.0, 2.0]) == 0 :
        windDirection = "WNW"
    elif cmp(windList, [5.0, 5.0, 5.0, 2.0]) == 0 :
        windDirection = "NW"
    elif cmp(windList, [5.0, 5.0, 3.0, 3.0]) == 0 :
        windDirection = "NNW"

    #print "Wind Direction: ", windDirection, "\t"
    #print "Temperature: ", round(float(temp.temperature), 2), "\t"
    lastTime = currentTime
    lastCount = currentCount
#   pushToPachube(sensor)
    #sys.stdout.flush()
    #print "\n",
    #sys.stdout.flush()
    time.sleep(1)

