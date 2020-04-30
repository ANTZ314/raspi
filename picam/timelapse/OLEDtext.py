# OLEDtext.py
# This Python code is meant for use with the Raspberry Pi and Adafruit's monochrome displays!
# This program is the simplest in the whole repo. All it does is prints 3 'Hello!'s in various forms on the OLED display.
# It illustrates how to change the font size and positioning of text on the OLED... As well as showing how to do
# basic text!
# This program was created by The Raspberry Pi Guy!

# Imports the necessary libraries... Gaugette 'talks' to the display ;-)
import gaugette.ssd1306
import gaugette.platform
import gaugette.gpio
import time
import sys

class OLEDtext:
	# The defined pin numbers must use the WiringPi pin numbering scheme.
	RESET_PIN = 15 		# WiringPi pin 15 is BCM_GPIO14.
	DC_PIN    = 16		# WiringPi pin 16 is BCM_GPIO15.

	spi_bus = 0
	spi_device = 0
	gpio = gaugette.gpio.GPIO()
	spi = gaugette.spi.SPI(spi_bus, spi_device)

	# Very important... This lets py-gaugette 'know' what pins to use in order to reset the display
	# Change rows & cols values depending on your display dimensions.
	led = gaugette.ssd1306.SSD1306(gpio, spi, reset_pin=RESET_PIN, dc_pin=DC_PIN, rows=32, cols=128) 

	def __initi__(self, **kwargs):
		print("init OLED")
	
	def clear_oled(self):
		self.led.begin()
		self.led.clear_display()
		self.led.display()
		self.led.invert_display()
		time.sleep(0.5)
		self.led.normal_display()
		time.sleep(0.5)
	
	def draw(self, interval, duration):
		inter = ""									# initialise string
		durat = ""								# initialise string
		
		text = 'TimeLapse!'							# allows 9 chars + !
		self.led.draw_text2(0,0,text,2)
			
		inter = "Interval: " + str(interval)
		print(inter)
		#text2= '1234567890123456789'				# allows 19 small across
		text2 = "Interval: " + str(interval)
		self.led.draw_text2(0,16,text2,1)
			
		durat = "Duration: " + str(duration)
		print(durat)
		#text2= '1234567890123456789'				# allows 19 small across
		text3 = "Duration: " + str(duration)
		self.led.draw_text2(0,25,text3,1)
		self.led.display()
		
	def clr_Space(self):
		inter = "      "
		durat = "      "
		
		#text2= '1234567890123456789'				# allows 19 small across
		text2 = "Interval: " + str(inter)
		self.led.draw_text2(0,16,text2,1)
		#text3= '1234567890123456789'				# allows 19 small across
		text3 = "Duration: " + str(durat)
		self.led.draw_text2(0,25,text3,1)
		self.led.display()
	
