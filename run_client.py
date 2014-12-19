#!/usr/bin/python        
# melvin.alvarado   

import sys
import socket               
from uuid import getnode as get_mac

mac = get_mac()

s = socket.socket()         
host = str(sys.argv[1])
#host = socket.gethostname() 
port = 2626

cmd = str(sys.argv[2])

print 'MAC:',mac
print 'HOST:',host

if cmd:
	try:
		s.connect((host, port))
		cmd = str(mac)+'.'+cmd
		print '[C] ' + cmd
		s.send(cmd)
		print s.recv(1024)
		s.close                    
	except:
		print 'Server is not responding'