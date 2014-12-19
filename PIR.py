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

class PIR:


	def __init__(self,pin=17):
		if(rpi_device):
			GPIO.setmode(GPIO.BCM)
			GPIO.setup(pin,GPIO.IN)
		self.pin = pin

	#def __del__(self):
		#logging.info('PIR releasing pins'		
		#if(rpi_device):GPIO.cleanup()

	def stop(self):
		self.event = True

	def wait_event(self):
		GPIO_PIR = self.pin
		self.event = False

		logging.info("  Waiting for PIR to settle..." )
		if(rpi_device):
			# Loops until PIR output is 0
			while GPIO.input(GPIO_PIR)==1:
				Current_State  = 0
		else:
			time.sleep(1)
		logging.info('  Ready!' )

		# Loops until event is detected
		while not self.event :

			# Read PIR state
			if(rpi_device):Current_State = GPIO.input(GPIO_PIR)
			else : 
				time.sleep(2)
				Current_State = 1

			if Current_State==1 :
				# PIR is triggered
				logging.info("  Motion detected!" )
				self.event = True
			else: 
				# Wait for 10 milliseconds
				time.sleep(0.01)




