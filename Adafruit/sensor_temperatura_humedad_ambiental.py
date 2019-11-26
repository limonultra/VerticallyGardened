# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 18:23:34 2019

@author: edusn
"""
import numpy as np
import board
import busio
import adafruit_sht31d

    i2c = busio.I2C(board.SCL, board.SDA)
    sensor = adafruit_sht31d.SHT31(i2c)
    
    loopcount = 0
    while True:
    print("\nTemperature: %0.1f C" % sensor.temperature)
    print("Humidity: %0.1f %%" % sensor.relative_humidity)
    loopcount += 1
    time.sleep(2)
    # every 10 passes turn on the heater for 1 second
    if loopcount == 10:
        loopcount = 0
        sensor.heater = True
        print("Sensor Heater status =", sensor.heater)
        time.sleep(1)
        sensor.heater = False
        print("Sensor Heater status =", sensor.heater)
   
    
    