# OLEDclock.py

# This program interfaces with one of Adafruit's OLED displays and a Raspberry Pi (over SPI). It displays the current 
# date (Day, Month, Year) and then scrolls to the current time. The program waits for 2 seconds between scrolls.

# Example code from the py-gaugette library... Commented by The Raspberry Pi Guy

# Imports the necessary modules
import gaugette.ssd1306
import gaugette.platform
import gaugette.gpio
import time
import sys

class OLEDClass:
	# Define which GPIO pins the reset (RST) and DC signals on the OLED display are connected to on the
	# Raspberry Pi. The defined pin numbers must use the WiringPi pin numbering scheme.
	RESET_PIN = 5 # WiringPi pin 15 is GPIO14.
	DC_PIN = 6 # WiringPi pin 16 is GPIO15.

	# Define the SPI comms parameters
	spi_bus = 0
	spi_device = 0
	gpio = gaugette.gpio.GPIO()
	spi = gaugette.spi.SPI(spi_bus, spi_device)

	# Very important... This lets py-gaugette 'know' what pins to use in order to reset the display
	led = gaugette.ssd1306.SSD1306(gpio, spi, reset_pin=RESET_PIN, dc_pin=DC_PIN, rows=32, cols=128) 
	offset = 0 # flips between 0 and 32 for double buffering
	
	def __init__(self, **kwargs):
		print("LED Class Init!!")

	def OLEDInitialise(self):
		# Change rows & cols values depending on your display dimensions.
		self.led.begin()
		self.led.clear_display()
		self.led.display()
		self.led.invert_display()
		time.sleep(0.5)
		self.led.normal_display()
		time.sleep(0.5)

	def OLEDClock(self):
		# write the current time to the display on every other cycle
		if self.offset == 0:
			text = time.strftime("%A")
			self.led.draw_text2(0,0,text,2)
			text = time.strftime("%e %b %Y")
			self.led.draw_text2(0,16,text,2)
			text = time.strftime("%X")
			self.led.draw_text2(0,32+4,text,3)
			self.led.display()
			time.sleep(1)
		else:
			time.sleep(1)

		# vertically scroll to switch between buffers
		for i in range(0,32):
			self.offset = (self.offset + 1) % 64
			self.led.command(self.led.SET_START_LINE | self.offset)
			time.sleep(0.01)
			
