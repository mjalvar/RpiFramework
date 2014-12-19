#!/usr/bin/python
# melvin.alvarado 

import time
import logging

try:
	import RPi.GPIO as GPIO
	rpi_device = True
except ImportError:
	rpi_device = False


class Servo:

	POS_DER = 2.5
	POS_IZQ = 12.5
	POS_NET = 7.5
	POS_ARR = 2.5
	POS_ABA = 12.5
	STEP = 0.0015


	def __init__(self,pin=4):
		if(rpi_device):
			GPIO.setmode(GPIO.BCM)
			GPIO.setup(pin,GPIO.OUT)
			self.p = GPIO.PWM(pin,50)
			self.p.start(self.POS_NET) 

		self.pin = pin
		self.p.ChangeDutyCycle(self.POS_NET)
		time.sleep(0.3)
		self.p.stop()


	def step_arriba(self):
		logging.info("Servo Arriba")
		self.p.ChangeDutyCycle(self.POS_ARR)
		time.sleep(self.STEP)
		self.p.stop()		

	def step_abajo(self):
		logging.info("Servo Abajo")
		self.p.ChangeDutyCycle(self.POS_ABA)
		time.sleep(self.STEP)
		self.p.stop()		

	def step_der(self):
		logging.info("Servo Derecha")
		self.p.ChangeDutyCycle(self.POS_DER)
		time.sleep(self.STEP)
		self.p.stop()		

	def step_izq(self):
		logging.info("Servo Izquierda")
		self.p.ChangeDutyCycle(self.POS_IZQ)
		time.sleep(self.STEP)
		self.p.stop()


	#def __del__(self):
		#logging.info('PIR releasing pins'		
		#if(rpi_device):GPIO.cleanup()	



	