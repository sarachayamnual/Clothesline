import serial
import RPi.GPIO as GPIO
import antolib
import os
import sys
import time

# Variable
hum = 60.0
temp = 30.5
weather = ""
state = ""
check = ""

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

# IFTTT
key = "dfyCMti4sTr8QYKQRk4ve984CF0_Ug4-s_7nSlqyQj3"
# send to google drive
def json_send_drive(value1,value2):
    data = '''curl -X POST -H "Content-Type: application/json" -d '{"value1":"%s","value2":"%s"}' https://maker.ifttt.com/trigger/hum_read/with/key/dfyCMti4sTr8QYKQRk4ve984CF0_Ug4-s_7nSlqyQj3'''%(value1,value2)
    print('sent to Google Drive')
    print data 
    os.system(data)
#sent to line notification
def json_send_line(value1,value2,value3):
    data = '''curl -X POST -H "Content-Type: application/json" -d '{"value1":"%s","value2":"%s","value3":"%s"}' https://maker.ifttt.com/trigger/Noti_Line/with/key/dfyCMti4sTr8QYKQRk4ve984CF0_Ug4-s_7nSlqyQj3'''%(value1,value2,value3)
    print('sent to Line Notification')
    print data 
    os.system(data)



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
    global temp
    global state
    global weather
    global check

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
                print('System: ON \n')
                print('clothesline: ON (Automatically)\n')
                json_send_line(state,weather,hum)
            else:
                clotheslineOff()
                print('System: ON \n')
                print('clothesline: OFF (Automatically)\n')
                json_send_line(state,weather,hum)
            print state
            check = "1"

        # Manual control    
        else:
            
            print state
            print('System: OFF \n')
            check = "0"

        # send data to google drive via IFTTT
        json_send_drive(hum,temp)

    # man control
    if(channel == 'clothesline'):
        value = int(msg)
        if(check == "0"):
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
    setup() 
    time.sleep(10)

       
anto.loop(myLoopFunction)

