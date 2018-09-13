import serial
import RPi.GPIO as GPIO
import antolib
import os
import sys
import time

# Prepare to exchange the data with Arduino
ser = serial.Serial('/dev/ttyACM0',9600)

# username of anto.io account
user = 'saracha_p'

# key of permission, generated on control panel anto.io
key = 'uneXPkFisdpIc5ROfAQnp0Kt3xM6UCYZLV2s6APL'

# your default thing.
thing = 'Clothesline'

# connect to Anto
anto = antolib.Anto(user, key, thing)

# FUNCTION

def ClotheslineOn():
    print('send1')
    ser.write("1")
    
def ClotheslineOff():
    print('send0')
    ser.write("0")


# Actually work

def connectedCB():
    print('in connectedcb')
    anto.sub("Clothesline");
 
def dataCB(channel, msg):
    print('in datacb')
    if(channel == 'Clothesline'):
        value = int(msg)
        if(value == 1):
            ClotheslineOn()
            print('Clothesline: ON\n')
        else:
            ClotheslineOff()
            print('Clothesline: OFF\n')

    

def setup():
    anto.mqtt.onConnected(connectedCB)
    anto.mqtt.onData(dataCB)
    anto.mqtt.connect()


def myLoopFunction():
    time.sleep(4)
    
setup()
anto.loop(myLoopFunction)

