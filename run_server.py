#!/usr/bin/python
# melvin.alvarado       

import subprocess
from time import sleep

from Config import Config

run_server = 'python '+ Config.FRAMEWORK_PATH +'/Server.py 1>&2'

while True:
	p = subprocess.Popen(run_server, stdout=subprocess.PIPE, shell=True)
	(output, err) = p.communicate()			
	sleep(5)
