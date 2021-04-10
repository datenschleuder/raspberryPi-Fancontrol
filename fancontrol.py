#!/usr/bin/env python3

# adapted from Edoardo Paolo Scalafiotti <edoardo849@gmail.com>
# https://hackernoon.com/how-to-control-a-fan-to-cool-the-cpu-of-your-raspberrypi-3313b6e7f92c

from time import sleep
import subprocess
import RPi.GPIO as GPIO
import logging
from datetime import datetime

# Adjust these settings for your environment
pin = 17
maxTMP = 65
minTMP = 40 
sleepTime = 5

logging.basicConfig( level=logging.INFO, filename='/var/log/fancontrol.log')

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.setwarnings(False)
    return()

def getCPUtemperature():
    res=subprocess.check_output(['vcgencmd', 'measure_temp']).decode("utf-8")
    temp = (res.replace("temp=","").replace("'C\n",""))
    #print("temp is {0}".format(temp))
    return temp

def fanON():
    setPin(True)
    return()
def fanOFF():
    setPin(False)
    return()
def getTEMP():
    CPU_temp = float(getCPUtemperature())
    now = datetime.now()
    if CPU_temp>maxTMP:
        logging.info(now.strftime("%d/%m/%Y %H:%M:%S")+' fan is activated at '+str(CPU_temp)+' degrees celsius')
        fanON()
    elif CPU_temp<minTMP:
        logging.info(now.strftime("%d/%m/%Y %H:%M:%S")+' fan is deactivated at '+str(CPU_temp)+' degrees celsius')
        fanOFF()
    return()
def setPin(mode):
    GPIO.output(pin, mode)
    return()

try:
    setup() 
    while True:
        getTEMP()
        sleep(sleepTime)
except KeyboardInterrupt: # trap a CTRL+C keyboard interrupt. Not needed for autorun but good for testing 
    GPIO.cleanup() # resets all GPIO ports used by this program
