#!/usr/bin/python
# melvin.alvarado

import time
import datetime
import os
import logging
import os.path
import re


class Config:

	DEBUG = False
	IS_RPI = True
	# DEBUG = True
	# IS_RPI = False

	if( DEBUG ):
		FRAMEWORK_PATH = '/home/mjalvar/Projects/RaspberryPi/framework'
	else:
		FRAMEWORK_PATH = '/home/pi/framework'


	def __init__(self,config_file='raspi.rc',user_file='.raspi.rc'):
		self.hash = {}
		if( os.path.exists(config_file) ):
			self.parser(config_file)
			if( os.path.exists(user_file) ):			
				self.parser(user_file)
		else:
			print '  cannot load config file '+config_file


	def parser(self,config_file):
		if( os.path.exists(config_file) ):		
			print '  reading config from '+config_file
			f = open(config_file,'r')
			for line in f:
				match = re.match( r'\s*(.*) = (.*)', line, re.M|re.I)
				if( match ):
					var = match.group(1)
					val = match.group(2)
					print '    ' + var + ' = ' + val
					num_match = re.match( r'^(\d+)$', val, re.M|re.I)
					if( num_match ):
						self.hash[var] = int(val)
					else:
						self.hash[var] = str(val)
		else:
			print '  cannot load config file '+config_file		


	def get(self,key):
		return self.hash[key]


	def get_bool(self,key):
		if( self.hash[key]=='True' ):
			return True
		else:
			return False

	def enable(self,key):
		return self.get_bool(key)

	def print_all(self):
		for k in sorted(self.hash.iterkeys()):
			logging.info( ' * ' + k + ' = ' + str(self.hash[k]) )

