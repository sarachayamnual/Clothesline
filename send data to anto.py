import serial
import RPi.GPIO as GPIO
import antolib
import os
import sys
import time

# Prepare to exchange the data with Arduino
# ser = serial.Serial('/dev/ttyACM0',9600)

# username of anto.io account
user = 'saracha_p'

# key of permission, generated on control panel anto.io
key = 'uneXPkFisdpIc5ROfAQnp0Kt3xM6UCYZLV2s6APL'

# your default thing.
thing = 'Clothesline'

# connect to Anto
anto = antolib.Anto(user, key, thing)

# Variable
hum = 50

# FUNCTION

# Actually work

def connectedCB():
    print('in connectedcb') 
    anto.sub("humidity");


def dataCB(channel, msg):
    print('in datacb')
    global hum
    
    print('humidity is')
    print hum
    anto.pub("humidity",hum)

    

def setup():
    anto.mqtt.onConnected(connectedCB)
    anto.mqtt.onData(dataCB)
    anto.mqtt.connect()


def myLoopFunction():
    time.sleep(4)
    
setup()
anto.loop(myLoopFunction)

