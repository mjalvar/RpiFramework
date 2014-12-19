#!/usr/bin/python
# melvin.alvarado   

import Config
import time
import threading
import logging

import os

from PIR import PIR
from Stream import Stream


class MotionAlarm:

	def __init__(self,camera,controls=None):
		self.event = threading.Event()
		self.sensor = PIR(pin=Config.PIN_PIR)
		self.is_running = True
		# self.stream = Stream(camera)
		self.camera = camera
		self.controls = controls
		self.Cnt = 1

		espeak_cmd = 'espeak -ves+m2 -f '+Config.FRAMEWORK_ROOT+'/alarm_on.txt --stdout | aplay'
		if Config.ALARM_ESPEAK:
			os.system(espeak_cmd)
		self.controls.system('aplay /home/pi/framework/alarm_on.wav')		

	def __del__(self):
		logging.info( 'MotionAlarm stopped' )


	def stop(self):
		self.is_running = False
		self.sensor.stop()
		# self.stream.stop()
		del(self.sensor)
		# del(self.stream)
		self.event.set()
		espeak_cmd = 'espeak -ves+m2 -f '+Config.FRAMEWORK_ROOT+'/alarm_off.txt --stdout | aplay'
		if Config.ALARM_ESPEAK:
			os.system(espeak_cmd)		
		self.controls.system('aplay /home/pi/framework/alarm_on.wav')	
		self.sleep(5)			



	def sleep(self,cnt):
		self.event.wait(cnt)


	def alarm(self):
		# self.stream.capture('/tmp/foto_tmp.jpg')
		self.controls.photo()

		Cmd = 'echo "'+Config.SERVER_NAME+' Alarma" | mail -a "' + '/var/www/foto.jpg' + '" -s "Raspi Alarma E' + str(self.Cnt) + '" ' + Config.ALARM_EMAILS
		if Config.ALARM_SEND_EMAIL:
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

				# t = threading.Thread(target=self.alarm)
				# t.start()	
				self.alarm()

				espeak_cmd = 'espeak -ves+m2 -f '+Config.FRAMEWORK_ROOT+'/alarm.txt --stdout | aplay'
				if Config.ALARM_ESPEAK:
					os.system(espeak_cmd)

				for x in xrange(10):
					self.controls.system('aplay /home/pi/framework/siren.wav')	

				self.sleep(5)
				self.controls.display('motion ready')



