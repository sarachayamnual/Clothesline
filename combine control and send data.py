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

# Variable
hum = 50.0
weather = "2222222222"
state = "555555555555"

# FUNCTION

def analysis():
    if(hum <= 80.0):
        global state
        global weather
        state = "on"
        anto.pub("state",state)
        weather = "clear"
        anto.pub("weather",weather)
    
    else:
        global state
        global weather
        state = "off"
        anto.pub("state",state)
        weather = "rain"
        anto.pub("weather",weather)

def clotheslineOn():
    # Arduino
    print('send 1')
    ser.write("1")

       
def clotheslineOff():
    # Arduino
    print('send 0')
    ser.write("0")

def bysystemOn():
    # Arduino
    print('send 1')
    ser.write("1")

def bysystemOff():
    # Arduino
    print('send 0')
    ser.write("0")

# Actually work

def connectedCB():
    print('in connectedcb')
    anto.sub("clothesline");
    anto.sub("collect");
    anto.sub("fan");
    anto.sub("humidity");
    anto.sub("state");
    anto.sub("system");
    anto.sub("temperature");
    anto.sub("weather");


def dataCB(channel, msg):
    print('in datacb')
    global hum
    global state
    global weather

    # system control
    if(channel == 'system'):
        value = int(msg)
        
        # Aanlysis
        analysis()

        # send humidity to anto
        anto.pub("humidity",hum)

        # Work automatically
        if(value == 1):
            if(state == 'on'):   
                clotheslineOn()
                print('clothesline: ON (Automatically)\n')
            else:
                clotheslineOff()
                print('clothesline: OFF (Automatically)\n')
            print state

        # Manual control    
        else:
            bysystemOff()
            print state
            print('clothesline: OFF (Manual)\n')

    # man control
    if(channel == 'clothesline'):
        value = int(msg)
        if(value == 1):
            bysystemOn()
            print state
            print('clothesline: ON (Manual)\n')
        else:
            bysystemOff()
            print state
            print('clothesline: OFF (Manual)\n')

def setup():
    anto.mqtt.onConnected(connectedCB)
    anto.mqtt.onData(dataCB)
    anto.mqtt.connect()


def myLoopFunction():
    time.sleep(10)
    
setup()
anto.loop(myLoopFunction)

