#!/usr/bin/python

import RPi.GPIO as GPIO
import time

from Servo import Servo


ele = Servo(pin=25)
rot = Servo(pin=24)

ele.step_arriba();




GPIO.cleanup()
