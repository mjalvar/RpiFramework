#!/usr/bin/python
# melvin.alvarado    

import sys
import os
import datetime
import time
import logging

try:
	import picamera
	from twython import Twython, TwythonError
	rpi_device = True
except ImportError:
	rpi_device = False


class Tweet:

	def __init__(self,text='',image=False,file_photo='/var/www/foto.jpg'):
		CONSUMER_KEY = 'TPcId3ZdR7jCYwec1A'
		CONSUMER_SECRET = '5eY3k8mEpHI0wCD2LSFK4y2b4zlMunbfc9zpEjdNU'
		ACCESS_KEY = '2273997643-dqvuxb4B2oOm2bFE0TKKMjXzt7vfCF7DZgy1HcW'
		ACCESS_SECRET = 'W9LcdB5qRh2dvWjbzR0C366nYQRPZq8f5RTOdvCZKuxFq'

		if(rpi_device):
			api = Twython(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_KEY,ACCESS_SECRET)
			
			if(text==''):
				date = datetime.datetime.now()
				text = date.strftime('%d %b %Y  %I:%M')

			if(image):	
				photo = open(file_photo,'rb')
				try:
					api.update_status_with_media(media=photo, status=text)
				except TwythonError as e:
					logging.error(e)

			else : 
				try:
					api.update_status_with_media(status=text)
				except TwythonError as e:
					logging.error(e)					
				
			logging.info('Tweet sent')
		else : logging.error('Twython lib not found')


