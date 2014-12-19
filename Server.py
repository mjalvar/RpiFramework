#!/usr/bin/python
# melvin.alvarado


import logging
import socket
import subprocess
import threading

import fcntl
import struct

from Config import Config
from Controls import Controls
from Tweet import Tweet


if( Config.IS_RPI ):
	try: 
		import RPi.GPIO as GPIO
	except ImportError:	
		logging.error("ERROR: Not a RPi device")			


class Server:
	"""Server"""

	module = {}
	mac_list = {
		'171859732747380':'raspi_naranjo',
		'159387612507493':'laptop_jossue',
		'140870679760510':'raspi_folsom',
	}


	def __init__(self):

		if( Config.DEBUG ):
			self.config = Config(
				config_file = Config.FRAMEWORK_PATH + '/raspi.rc',
				user_file = '/home/mjalvar/.raspi.rc'
			)
		else:
			self.config = Config(
				config_file = '/home/pi/framework/raspi.rc',
				user_file = '/home/pi/.raspi.rc'
			)			

		logging.basicConfig(
			filename=self.config.get('SERVER_LOG'),
			filemode='w',
			format='%(asctime)s - %(filename)s: %(message)s',
			level=logging.INFO
		) 
		logging.info('===================================================')

		self.s = socket.socket()         
		host = '0.0.0.0'
		port = self.config.get('SERVER_PORT')
		self.name = self.config.get('SERVER_NAME')
		self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)		
		self.s.bind((host, port))

		# Event
		self.event = threading.Event()
		self.ext_ip = '0.0.0.0'
		self.getIP_cmd()

		self.config.print_all()
		logging.info('Creating server %s at %s:%s' % (self.name,host,port))
		self.cmd = Controls( config=self.config )
		self.run()


	def run(self):
		s = self.s
		s.listen(5)
		self.is_running = True

		logging.info('Starting server...')
		self.cmd.display('Hello')
		self.cmd.beep()
		self.getExternalIP()

		# Sending Hello World
		# FIXME tweet = Tweet(image=True,text=ext_ip)
		self.cmd.display('Ready',str(self.ext_ip))

		logging.info('Ready')

		# Main loop
		while self.is_running:
			c, addr = s.accept()    
			logging.info('[R] Req from' + str(addr) )
			req = c.recv(1024)
   			logging.info('[R] %s' % req)
			rsp = self.check(req)   			
   			if( rsp ) : c.send(rsp)
			else: c.send('Not supported')		
			c.close()
		s.shutdown(1)
		s.close()

		# Actions before stop
		self.cmd.stop()
		if( Config.IS_RPI ) : 
			GPIO.cleanup()			


	def check(self,req):
		arr = req.split('.')
		device = self.mac_list.get(arr[0],0)
		req = str(arr[1])
		req = req.rstrip('\n')

		if( not device ) : return False

		logging.info('[D] Device %s' % device)
		logging.info('[C] %s' % req)
		self.cmd.display(t1=req)

		if( req == 'restart' ):
			self.is_running = False
			if( Config.IS_RPI ) : GPIO.cleanup()	
			return 'Restarting'
		else:
			if( req=='status' or req=='list' ): rsp = self.cmd.run(req,wait=True)
			else : rsp = self.cmd.run(req)
			if( rsp ):
				if( req=='status'): self.cmd.display(t2=rsp)
				logging.info('[>] %s'%rsp)
				return str(rsp)
		return False


	def getExternalIP(self):
		t = threading.Thread(target=self.getExternalIP_cmd, args=())
		t.start()
		self.wait(5)

	def getExternalIP_cmd(self):
		p = subprocess.Popen("curl -s http://ipecho.net/plain", stdout=subprocess.PIPE, shell=True)
		(output, err) = p.communicate()		
		self.ext_ip = output
		self.event.set()

	def getIP_cmd(self):
		ip = self.get_ip_address('wlan0')
		logging.info("IP: %s" % ip)
		self.ext_ip = ip

	def get_ip_address(self,ifname):
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		return socket.inet_ntoa(fcntl.ioctl(
			s.fileno(),
			0x8915,  # SIOCGIFADDR
			struct.pack('256s', ifname[:15])
		)[20:24])	

	def wait(self,cnt):
		self.event.wait(cnt)		


if __name__ == '__main__':
	server = Server()
           
