#!/usr/bin/python
# melvin.alvarado       

import Config
import subprocess


def system(cmd,wait=True):
	p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
	if(wait):(output, err) = p.communicate()
	return output

dpkg_deb = 'dpkg-deb -z8 -Zgzip --build RaspiFramework'
system('cd /home/mjalvar/Projects && '+dpkg_deb)
system('mv /home/mjalvar/Projects/*.deb /var/www/raspi')
system('chmod 755 /var/www/raspi/ -R')