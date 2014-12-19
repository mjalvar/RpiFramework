#!/usr/bin/python
# melvin.alvarado       

import subprocess
from time import sleep
import logging


from Config import Config


print 'Starting...'
my_config = Config(
				config_file = '/home/mjalvar/Projects/RaspiFramework/home/pi/framework/raspi.rc',
				user_file = '/home/mjalvar/.raspi.rc'
			)

print 'log is ' + my_config.get('SERVER_LOG')


my_config.print_all()