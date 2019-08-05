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

# Define which GPIO pins the reset (RST) and DC signals on the OLED display are connected to on the
# Raspberry Pi. The defined pin numbers must use the WiringPi pin numbering scheme.
RESET_PIN = 15 		# WiringPi pin 15 is BCM_GPIO14.
DC_PIN    = 16		# WiringPi pin 16 is BCM_GPIO15.

spi_bus = 0
spi_device = 0
gpio = gaugette.gpio.GPIO()
spi = gaugette.spi.SPI(spi_bus, spi_device)

# Very important... This lets py-gaugette 'know' what pins to use in order to reset the display
led = gaugette.ssd1306.SSD1306(gpio, spi, reset_pin=RESET_PIN, dc_pin=DC_PIN, rows=32, cols=128) # Change rows & cols values depending on your display dimensions.
led.begin()
led.clear_display()
led.display()
led.invert_display()
time.sleep(0.5)
led.normal_display()
time.sleep(0.5)

def main():
	try:
		text = 'TimeLapse!'				# allows 9 chars + !
		led.draw_text2(0,0,text,2)
			
		#text2= '1234567890123456789'	# allows 19 small across
		text2 = 'Interval: 5sec'
		led.draw_text2(0,16,text2,1)

		#text2= '1234567890123456789'	# allows 19 small across
		text3 = 'Frames:   150'
		led.draw_text2(0,25,text3,1)
		led.display()
		
		time.sleep(3)
		
		text = 'TimeLapse!'				# allows 9 chars + !
		led.draw_text2(0,0,text,2)
			
		#text2= '1234567890123456789'	# allows 19 small across
		text2 = 'Interval: 10sec'
		led.draw_text2(0,16,text2,1)

		#text2= '1234567890123456789'	# allows 19 small across
		text3 = 'Frames:   200'
		led.draw_text2(0,25,text3,1)
		led.display()
		
		sys.exit(0)
			
	# Ctrl+C will exit the program correctly
	except KeyboardInterrupt:
		print("\r\nEXIT PROGRAM!!")
		GPIO.cleanup()								# Kill Batmans parents
		sys.exit(0)									# Take Martha's pearls

if __name__ == "__main__":
	main()
