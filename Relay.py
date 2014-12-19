#!/usr/bin/python
# melvin.alvarado 

import time
import datetime
import os
import logging

try:
	import RPi.GPIO as GPIO
	rpi_device = True
except ImportError:
	rpi_device = False

class Relay:

	def __init__(self,pin=22):
		if(rpi_device):
			GPIO.setmode(GPIO.BCM)
			GPIO.setup(pin,GPIO.OUT)
		GPIO_RELAY = pin

		logging.info("  Relay Set" )
		if(rpi_device):
			GPIO.output(GPIO_RELAY,False)
			time.sleep(1.8)
			GPIO.output(GPIO_RELAY,True)
	




