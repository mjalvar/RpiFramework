#!/usr/bin/python
# melvin.alvarado       

import Config
import subprocess

def system(cmd,wait=True):
	p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
	if(wait):(output, err) = p.communicate()
	return output

wget = 'wget http://'+Config.MIRROR_IP+'/raspi/RaspiFramework.deb -O /tmp/RaspiFramework.deb'
system(wget)
system('dpkg -i /tmp/RaspiFramework.deb')