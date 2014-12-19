#!/usr/bin/python
# Import required Python libraries
import time
import logging
import RPi.GPIO as GPIO


class UltraSonic:

	def __init__(self, trigger=11, echo=9):

		# Use BCM GPIO references
		# instead of physical pin numbers
		GPIO.setmode(GPIO.BCM)

		# Define GPIO to use on Pi
		GPIO_TRIGGER = trigger
		self.pin_trigger = trigger
		GPIO_ECHO    = echo
		self.pin_echo = echo

		logging.debug("Ultrasonic Measurement")

		# Set pins as output and input
		GPIO.setup(GPIO_TRIGGER,GPIO.OUT)  # Trigger
		GPIO.setup(GPIO_ECHO,GPIO.IN)      # Echo

	def read(self):
		GPIO_TRIGGER = self.pin_trigger
		GPIO_ECHO = self.pin_echo

		# Set trigger to False (Low)
		GPIO.output(GPIO_TRIGGER, False)

		# Allow module to settle
		time.sleep(0.5)

		# Send 10us pulse to trigger
		GPIO.output(GPIO_TRIGGER, True)
		time.sleep(0.00001)
		GPIO.output(GPIO_TRIGGER, False)
		start = time.time()

		while GPIO.input(GPIO_ECHO)==0:
		  start = time.time()

		while GPIO.input(GPIO_ECHO)==1:
		  stop = time.time()

		# Calculate pulse length
		elapsed = stop-start

		# Distance pulse travelled in that time is time
		# multiplied by the speed of sound (cm/s)
		distance = elapsed * 34300

		# That was the distance there and back so halve the value
		distance = distance / 2

		logging.debug("Distance : %.1f cm" % distance)
		return distance

		# Reset GPIO settings
		# GPIO.cleanup()


if __name__ == '__main__':
	sensor = UltraSonic()
	distance = sensor.read()
	print "Distance : %.1f cm" % distance	
