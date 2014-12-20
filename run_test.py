#!/usr/bin/python
# melvin.alvarado       

import subprocess
from time import sleep
import logging
import datetime

from Config import Config



print 'Starting...'
now = datetime.datetime.now()
print 'Hoy es ' + str(now.hour)