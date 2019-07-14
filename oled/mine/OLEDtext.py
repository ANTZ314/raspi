# -*- coding: utf-8 -*-
"""
Description:
This Python code is meant for use with the Raspberry Pi and Adafruit's monochrome displays!
All it does is prints 3 'Hello!'s in various forms on the OLED display.

Run the program like this:
$ python OLEDtext.py 
"""
# Gaugette 'talks' to the display
import gaugette.ssd1306
import gaugette.platform
import gaugette.gpio
import time
import sys

# The defined pin numbers must use the WiringPi pin numbering scheme
RESET_PIN = 15 							# WiringPi pin 15 is GPIO14.
DC_PIN = 16 							# WiringPi pin 16 is GPIO15.

spi_bus = 0
spi_device = 0
gpio = gaugette.gpio.GPIO()
spi = gaugette.spi.SPI(spi_bus, spi_device)

# Very important... This lets py-gaugette 'know' what pins to use in order to reset the display
led = gaugette.ssd1306.SSD1306(gpio, spi, reset_pin=RESET_PIN, dc_pin=DC_PIN, rows=32, cols=128)
led.begin()
led.clear_display()
led.display()
led.invert_display()
time.sleep(0.5)
led.normal_display()
time.sleep(0.5)

# led.draw_text2(x-axis, y-axis, whatyouwanttoprint, size)
# So led.drawtext2() prints simple text to the OLED display like so:

text = 'TimeLapse!'				# allows 9 chars + !
led.draw_text2(0,0,text,2)

#text2= '1234567890123456789'	# allows 19 small across
text2 = 'Interval: 5sec'
led.draw_text2(0,16,text2,1)

#text2= '1234567890123456789'	# allows 19 small across
text3 = 'Frames:   150'
#led.draw_text2(32,25,text3,1)
led.draw_text2(0,25,text3,1)
led.display()
