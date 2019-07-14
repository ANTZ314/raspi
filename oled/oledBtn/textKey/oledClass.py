# -*- coding: utf-8 -*-
"""
Description:
OLED display functions
"""
# Imports the necessary modules
import gaugette.ssd1306
import gaugette.platform
import gaugette.gpio
import time
import sys

class OLEDClass:
	# Define which GPIO pins the reset (RST) and DC signals on the OLED display are connected to on the
	# Raspberry Pi. The defined pin numbers must use the WiringPi pin numbering scheme.
	RESET_PIN 	= 6 # WiringPi pin 15 is GPIO14.
	DC_PIN 		= 5 # WiringPi pin 16 is GPIO15.

	# Define the SPI comms parameters
	spi_bus = 0
	spi_device = 0
	gpio = gaugette.gpio.GPIO()
	spi = gaugette.spi.SPI(spi_bus, spi_device)

	# Very important... This lets py-gaugette 'know' what pins to use in order to reset the display
	led = gaugette.ssd1306.SSD1306(gpio, spi, reset_pin=RESET_PIN, dc_pin=DC_PIN, rows=32, cols=128) 
	offset = 0 # flips between 0 and 32 for double buffering
	
	def __init__(self, **kwargs):
		print("OLED Class Init!!")

	def OLEDInitialise(self):
		# Change rows & cols values depending on your display dimensions.
		self.led.begin()
		self.led.clear_display()
		self.led.display()
		self.led.invert_display()
		time.sleep(0.5)
		self.led.normal_display()
		time.sleep(0.5)

	def OLEDtext1(self):
		# led.draw_text2(x-axis, y-axis, whatyouwanttoprint, size) < Understand?
		# So led.drawtext2() prints simple text to the OLED display like so:
		text = 'SecuriCam: '
		self.led.draw_text2(0,0,text,2)
		text2 = 'Option 1 <--'
		self.led.draw_text2(0,16,text2,1)
		text3 = 'Option 2    '
		self.led.draw_text2(0,25,text3,1)
		self.led.display()
			
	def OLEDtext2(self):
		# led.draw_text2(x-axis, y-axis, whatyouwanttoprint, size) < Understand?
		# So led.drawtext2() prints simple text to the OLED display like so:
		text = 'SecuriCam: '
		self.led.draw_text2(0,0,text,2)
		text2 = 'Option 1    '
		self.led.draw_text2(0,16,text2,1)
		text3 = 'Option 2 <--'
		self.led.draw_text2(0,25,text3,1)
		self.led.display()
		
		
