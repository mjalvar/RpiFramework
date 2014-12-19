#!/usr/bin/python
# melvin.alvarado   

import time
import threading
import logging

import os

from PIR import PIR
from Stream import Stream
from Config import Config


class MotionAbuela:

	def __init__(self,camera,config,controls=None):
		self.event = threading.Event()
		self.sensor = PIR(pin=config.get('PIN_PIR'))
		self.is_running = True
		# self.stream = Stream(camera)
		self.camera = camera
		self.controls = controls
		self.config = config
		self.Cnt = 1

		self.controls.system('aplay /home/pi/framework/alarm_on.wav')		

	def __del__(self):
		logging.info( 'MotionAbuela stopped' )


	def stop(self):
		self.is_running = False
		self.sensor.stop()
		# self.stream.stop()
		del(self.sensor)
		# del(self.stream)
		self.event.set()
		self.controls.system('aplay /home/pi/framework/alarm_on.wav')	
		self.sleep(5)			



	def sleep(self,cnt):
		self.event.wait(cnt)


	def alarm(self):
		config = self.config
		self.controls.photo()

		Cmd = Config.FRAMEWORK_PATH + '/run_client.py ' + config.get('ABUELA_BEEP_HOST') + ' ' + str(config.get('ABUELA_BEEP_PORT')) + ' ' + 'beep'
		logging.info( 'Beep Cmd: ' + Cmd )
		os.system(Cmd)


		Cmd = 'echo "'+self.config.get('SERVER_NAME')+' Abuela" | mail -a "' + '/var/www/foto.jpg' + '" -s "Raspi Abuela E' + str(self.Cnt) + '" ' + self.config.get('ABUELA_EMAILS')
		if self.config.enable('ABUELA_SEND_EMAIL'):
			logging.info(Cmd)
			os.system(Cmd)

		self.Cnt = self.Cnt + 1
		logging.info( 'Correo enviado...' )

	

	def run(self):
		logging.info( 'Alarm starting...' )
		# self.stream.run()
		while self.is_running:
			self.sensor.wait_event()
			self.controls.display('motion detected')
			if(self.is_running):

				self.alarm()

				self.sleep(5)
				self.controls.display('motion ready')



