#!/usr/bin/python
# melvin.alvarado     

import subprocess
import socket
import time
import threading

import logging

from Config import Config

if( Config.IS_RPI ):
	try: 
		import picamera
	except ImportError:	
		logging.error("ERROR: Not a RPi device")		


class Stream:

	def __init__(self,camera,config):
		self.main_cmd = "sudo -u pi python /home/pi/framework/Stream.py"
		self.event = threading.Event()		
		self.camera = camera
		self.config = config


	def run(self):
		if( Config.IS_RPI ):
			self.event.clear()
			self.system(self.main_cmd,wait=False)		
			time.sleep(3)
			t = threading.Thread(target=self.cvlc, args=())
			t.start()			


	def system(self,cmd,wait=True):
		logging.info('system: %s'%cmd)
		p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
		if(wait):(output, err) = p.communicate()
		return 


	def capture(self,capture_file='/tmp/foto.jpg'):
		if( Config.IS_RPI ):
			logging.info('Capturing photo')			
			self.camera.capture(capture_file,resize=(self.config.get('PHOTO_W'),self.config.get('PHOTO_H')),use_video_port=True)


	def cvlc(self):

		camera =  self.camera

		try:
			client_socket = socket.socket()
			client_socket.connect(('localhost', 9000))	
			connection = client_socket.makefile('wb')	

			camera.resolution = (2592, 1944)
			# Start a preview and let the camera warm up for 2 seconds
			camera.start_preview()
			time.sleep(2)
			# Start recording, sending the output to the connection for 60
			# seconds, then stop
			camera.start_recording(connection, format='h264',resize=(self.config.get('VIDEO_W'), self.config.get('VIDEO_H')))
			#camera.wait_recording(5)
			self.event.wait()
			camera.stop_recording()

			connection.close()
			client_socket.close()

		except:
			logging.error("No connection to local socket for vlc transmition")


	def kill(self,word):
		self.system('pkill -f '+word)

	def stop(self):
		self.event.set()		
		self.kill('vlc')
		self.kill('nc')
		#self.kill('Stream.py')
		#self.kill('raspistill')
		#self.kill('raspivid')
		#self.kill('vlc')

if __name__ == '__main__':

	if( Config.DEBUG ):
		config = Config(
			config_file = Config.FRAMEWORK_PATH + '/raspi.rc',
			user_file = '/home/mjalvar/.raspi.rc'
		)
	else:
		config = Config(
			config_file = '/home/pi/framework/raspi.rc',
			user_file = '/home/pi/.raspi.rc'
		)	

	vlc_stream = "nc -l 9000 | sudo -u pi cvlc stream:///dev/stdin --sout '#standard{access=http,mux=ts,dst=:"+str(config.get('VLC_PORT'))+"}' :demux=h264 2> /dev/null"
	p = subprocess.Popen(vlc_stream, stdout=subprocess.PIPE, shell=True)
	#(output, err) = p.communicate()
