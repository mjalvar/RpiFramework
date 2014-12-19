#!/usr/bin/python
# melvin.alvarado 

import sys
import logging
from time import sleep

from Config import Config

if( Config.IS_RPI ):
    try:
        import RPi.GPIO as GPIO
    except ImportError:
        logging.error("ERROR: Not a RPi device")


class Display:
    """ Support for HD44780 display"""

    data = ['','']

    def __init__(self, pin_rs=7, pin_e=8, pins_db=[25,24,23,18]):

        if( rpi_device ):
            self.pin_rs = pin_rs
            self.pin_e = pin_e
            self.pins_db = pins_db

            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.pin_rs,GPIO.OUT)
            GPIO.setup(self.pin_e,GPIO.OUT)

            for pin in self.pins_db:
                GPIO.setup(pin,GPIO.OUT)

            self.clear()


    #def __del__(self):
        #print 'Display releasing pins'
        #if( rpi_device ): GPIO.cleanup()


    def clear(self):
        """ Blank/Reset LCD"""

        self.cmd(0x33)
        self.cmd(0x32)
        self.cmd(0x28)
        self.cmd(0x0C)
        self.cmd(0x06)
        self.cmd(0x01)


    def cmd(self,bits,char_mode=False):
        """ Send command to LCD"""

        if( rpi_device ):
            sleep(0.0012)
            bits = bin(bits)[2:].zfill(8)
            GPIO.output(self.pin_rs,char_mode)

            for pin in self.pins_db:
                GPIO.output(pin,False)

            for i in range(4):
                if bits[i] == "1":
                    GPIO.output(self.pins_db[::-1][i],True)
                
            GPIO.output(self.pin_e,True)
            GPIO.output(self.pin_e,False)

            for pin in self.pins_db:
                GPIO.output(pin,False)
            
            for i in range(4,8):
                if bits[i] == "1":
                    GPIO.output(self.pins_db[::-1][i-4],True)

            GPIO.output(self.pin_e,True)
            GPIO.output(self.pin_e,False)


    def message(self, text):
        """ Send String to LCD. Newline wraps to 2nd line """

        if( rpi_device ):
            self.clear()
            for char in text:
                if char == '\n' or char == '^':
                    self.cmd(0xC0)  # new line
                else:
                    self.cmd(ord(char),True)


    def line(self, number, text, send=True):
        """Writing a specific line"""
        data = self.data
        i = number-1
        data[i] = text
        text = data[0]+'^'+data[1]

        if( rpi_device and send ): self.message(text)
        if( send ):
            logging.debug( "================" )
            logging.debug( "%s" % data[0] )
            logging.debug( "%s" % data[1] )
            logging.debug( "================" )


if __name__ == '__main__':

    dis = Display()
    if len(sys.argv)>1:
        dis.message(sys.argv[1])
    else:
        dis.message("Puede poner\nun parametro")
            
    
