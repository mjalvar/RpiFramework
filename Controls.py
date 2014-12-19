#!/usr/bin/python
# melvin.alvarado     

import subprocess
import threading
import time
import logging
import datetime
import os

from Config import Config
from Display import Display 


if( Config.IS_RPI ):
	try:
		import picamera
		from MotionTweet import MotionTweet
		from MotionAlarm import MotionAlarm
		from Relay import Relay
		from Tweet import Tweet
		from Servo import Servo
		from Stream import Stream		
	except ImportError:
		logging.error("ERROR: Not a RPi device")	



class Controls:

	status = {
		'camera' : 0,
		'motion_tweet' : 0,
		'motion_alarm' : 0,
		'relay' : 0,
		'display' : 0,
		'servo' : 0,
	}
	execute = {}


	def __init__(self,config):

		self.config = config
		self.mirror = config.get('MIRROR_IP')

		# Commands
		self.execute['list'] = self.list							# list supported commands
		self.execute['status'] = self.get_status					# send status
		self.execute['restart_machine'] = self.restart				# restart machine
		self.execute['poweroff_machine'] = self.poweroff			# 
		self.execute['update'] = self.update						# download files from mirror 

		if( config.enable('CAMERA') ) : 
			self.execute['photo'] = self.photo						# take a photo
			self.execute['tweet'] = self.tweet						# take a photo, send a tweet			
		if( config.enable('SOUND') ) : 
			self.execute['beep'] = self.beep						# play beep.wav
		if( config.enable('RELAY') ) : 
			self.execute['relay'] = self.relay						# trigger RelayEn
		if(config.enable('MOTION') and config.enable('CAMERA')) : 
			self.execute['start_tweet'] = self.start_motion_tweet	# tweet triggered by MotionEn
			self.execute['stop_tweet'] = self.stop_motion_tweet	
			self.execute['start_alarm'] = self.start_motion_alarm	# alarm triggered by MotionEn
			self.execute['stop_alarm'] = self.stop_motion_alarm			
		if( config.enable('SERVO') ):
			self.execute['pos_ventana'] = self.pos_ventana
			self.execute['pos_adentro'] = self.pos_adentro

		logging.info('Supported commads:')
		for k in self.execute:
			logging.info('\t%s'%k)

		# Common resources
		self.sem = threading.BoundedSemaphore(value=1)
		if( Config.IS_RPI  and config.enable('CAMERA') ): 
			self.Camera = picamera.PiCamera()
			self.Stream = Stream(self.Camera,self.config)
			self.Stream.run()			
		else: 
			self.Camera = None
			self.Stream = None

		if( config.enable('DISPLAY')  ) : self.Display = Display( pin_rs=7, pin_e=8, pins_db=[25,24,23,18] )
		else: self.Display = None


	def stop(self):
		self.stop_motion_tweet()
		self.stop_motion_alarm()
		if( self.Stream ):
			self.Stream.stop()


	def run(self,cmd,args='',wait=False):
		cmd = cmd.rstrip('\n')
		if( self.execute.get(cmd,args) ):
			if( wait ):
				rsp = self.execute[cmd](args)
				return str(rsp)
			else:
				t = threading.Thread(target=self.execute[cmd], args=(args,))
				t.start()				
				return 'OK'
		else: 
			logging.info('Command %s not supported'%cmd) 
			return 0


	# =======================================
	# Servo
	def pos_ventana(self,args=''):
		if( self.grab('servo') ):
			Servo = Servo()
			Servo.ventana()
			self.release('servo')

	def pos_adentro(self,args=''):
		if( self.grab('servo') ):
			Servo = Servo()
			Servo.adentro()
			self.release('servo')			


	# =======================================
	# Utilities
	def system(self,cmd,wait=True):
		logging.info('system: %s',cmd)
		p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
		if(wait):(output, err) = p.communicate()
		return output

	def grab(self,cmd):
		if( self.status[cmd] == 1 ) : return 0;
		else:
			self.sem.acquire()
			self.status[cmd] = 1
			self.sem.release()
			return 1

	def release(self,cmd):
		self.status[cmd] = 0

	def is_active(self,cmd):
		return self.status[cmd]


	# =======================================
	# Display control
	def display(self,t1='',t2=''):
		Display = self.Display
		if( self.grab('display') ):		
			if( Display and (not t1=='' or not t2=='') ) : 
				if t2=='' :
					Display.line(number=1,text=t1,send=True)
				if t1=='':
					Display.line(number=2,text=t2,send=True)
				if not t1=='' and not t2=='':	
					Display.line(number=1,text=t1,send=False)
					Display.line(number=2,text=t2,send=True)
			self.release('display');		


	# =======================================
	# Status
	def get_status(self,args):
		status_str = 'C:'+str(self.status['camera'])
		status_str = status_str+' T:'+str(self.status['motion_tweet'])
		status_str = status_str+' A:'+str(self.status['motion_alarm'])
		return status_str

	def list(self, args):
		rsp = ''
		for k in self.execute:
			rsp = k+' '+rsp
		return rsp		


	# =======================================
	# System
	def restart(self,args):
		self.system('reboot')

	def poweroff(self,args):
		self.system('poweroff')		

	def beep(self,args=''):
		if( self.config.enable('SOUND')  ):
			self.system('aplay '+ Config.FRAMEWORK_PATH +'/beep.wav')

	def update(self,args):
		deb_file = '/tmp/RaspiFramework.deb'
		logging.info('Updating from: %s'%self.mirror)
		wget = 'wget http://'+self.mirror+'/raspi/RaspiFramework.deb -O '+deb_file
		if os.path.exists(deb_file):
			os.remove(deb_file)
		self.system(wget)
		#fileinfo = os.stat(deb_file)
		#logging.info('File size: '+fileinfo.st_size)
		self.system('dpkg -i /tmp/RaspiFramework.deb')
		logging.info('Updating done')


	# =======================================
	# Relay
	def relay(self,args):
		if( self.grab('relay') ):
			my_relay = Relay()
			self.release('relay')


	# =======================================
	# Motion Tweet
	def tweet(self,args=''):
		self.photo()		
		tweet = Tweet(image=True)
		
	def start_motion_tweet(self,args=''):
		if( self.grab('camera') and self.grab('motion_tweet') ):
			self.motion_tweet = MotionTweet(camera=self.Camera,controls=self)
			self.motion_tweet.run()

	def stop_motion_tweet(self,args=''):
		if( self.is_active('motion_tweet') ):
			self.motion_tweet.stop()
			del(self.motion_tweet)
		self.release('camera')
		self.release('motion_tweet')


	# =======================================
	# Motion Alarm
	def start_motion_alarm(self,args=''):
		if( self.grab('camera') and self.grab('motion_alarm') ):
			self.motion_alarm = MotionAlarm(camera=self.Camera,controls=self)
			self.motion_alarm.run()

	def stop_motion_alarm(self,args=''):
		if( self.is_active('motion_alarm') ):
			self.motion_alarm.stop();
			del(self.motion_alarm)
		self.release('camera')
		self.release('motion_alarm')



	# =======================================
	# Photo Capture
	def photo(self, args=''):
		# w = 400
		# h = 300

		if( self.Stream ):

			logging.info('Photo starting')						
			self.Stream.capture('/tmp/foto_tmp.jpg')
			# Camera.resolution = (w, h)
			# Camera.start_preview()
			# # Camera warm-up time
			# time.sleep(2)
			# Camera.capture('/tmp/foto_tmp.jpg')			

			self.photo_wm()
			# self.release('camera')
			logging.info('Photo done')

		return 


	def photo_wm(self, args='',file_photo='/tmp/foto_tmp.jpg'):
		w = self.config.get('PHOTO_W')
		h = self.config.get('PHOTO_H')
		w_str = str(w)
		h_str = str(h)

		con_w = str(w*350/800)
		con_h = str(h*580/600)
		con_ps = str(25*w/800)

		today = datetime.datetime.now()
		today_string = today.strftime('%d %b %Y  %I:%M')

		logging.info('WM starting')
		convert = 'convert -size '+w_str+'x'+h_str+' xc:transparent -font Courier-bold -pointsize '+con_ps+' -fill White -draw "text '+con_w+','+con_h+' \''+today_string+'\'" /tmp/wm.png'
		self.system(convert)

		composite = 'composite -dissolve 50% -quality 100 /tmp/wm.png ' +file_photo+ ' /var/www/foto.jpg'
		self.system(composite)

		convert = 'convert /var/www/foto.jpg -resize 400x300 /var/www/foto_tn.jpg'
		self.system(convert)

		logging.info('WM done')

