#!/usr/bin/python
# melvin.alvarado   

import Config
import time
import threading
import logging

from Tweet import Tweet
from PIR import PIR
from Stream import Stream


class MotionTweet:

	def __init__(self,camera,config,controls=None):
		self.event = threading.Event()
		self.sensor = PIR(pin=config.get('PIN_PIR'))
		self.is_running = True
		# self.stream = Stream(camera)
		self.camera = camera
		self.controls = controls
		self.config = config

	def __del__(self):
		logging.info( 'MotionTweet stopped' )


	def stop(self):
		self.is_running = False
		self.sensor.stop()
		# self.stream.stop()
		del(self.sensor)
		# del(self.stream)
		self.event.set()


	def sleep(self,cnt):
		self.event.wait(cnt)


	def run(self):

		# self.stream.run()
		while self.is_running:
			self.sensor.wait_event()
			self.controls.display('motion detected')
			if(self.is_running):
				# self.controls.pos_adentro()
				logging.info('Capturing photo')							
				# self.stream.capture('/tmp/foto_tmp.jpg')
				self.controls.photo()
				# self.controls.photo_wm()
				tweet = Tweet(image=True)
				self.sleep(self.config.get('TWEET_SLEEP'))
				# self.controls.pos_ventana()					
				self.controls.display('motion ready')



