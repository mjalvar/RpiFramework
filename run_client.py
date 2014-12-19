#!/usr/bin/python        
# melvin.alvarado   

import sys
import socket               
from uuid import getnode as get_mac

mac = get_mac()

s = socket.socket()         
host = str(sys.argv[1])
port = str(sys.argv[2])
#host = socket.gethostname() 
#port = 2626

cmd = str(sys.argv[3])

print 'MAC= ',mac
print 'HOST= ',host,':',port
print 'CMD= ',cmd


if cmd:
	try:
		s.connect((host, int(port)))
		cmd = str(mac)+'.'+cmd
		print '[C] ' + cmd
		s.send(cmd)
		print s.recv(1024)
		s.close                    
	except:
		print 'Server is not responding'