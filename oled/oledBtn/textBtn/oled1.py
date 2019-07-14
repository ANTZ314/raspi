#!/usr/bin/env python
"""
# -*- coding: utf-8 -*-
Description:
PyImageSearch Surveillance Example edited out DropBox storage

USAGE:
$ python security1.py --conf conf1.json
"""
# import the necessary packages
import sys
import btnClass as btn
import ledClass as leds
import oledClass as oled
import RPi.GPIO as GPIO

###################
## MAIN FUNCTION ##
###################
def main():
	LEDS = leds.LEDClass()												# LED control class 
	OLED = oled.OLEDClass()												# Instantiate OLED Class
	BTN  = btn.btnClass()												# Instantiate Btn Class
	
	once1 = 1
	once2 = 1
	
	print "LET'S BEGIN!!"
	LEDS.All_Off1()														# LED 1 Off
	LEDS.All_Off2()														# LED 2 Off
	print "Start-up Mode:"
	
	# Any main exceptions:
	try:
		try:
			OLED.OLEDInitialise()
			
			while True:
				if BTN.Btn1() == 1:										# Btn 1 pressed
					if once1 == 1:
						once1 = 0										# shift option
						OLED.OLEDtext1()								# Option 1
						print"First Menu Option!!"
					else:
						once1 = 1										# shift option
						OLED.OLEDtext2()								# Option 2
						print"Second Menu Option!!"
					LEDS.Blink_Purple1()								# indicate btn press
					
						
		# Ctrl+C will exit the program correctly:
		except KeyboardInterrupt:
			print("\r\nEXIT PROGRAM!!")									# Pistol whip Thomas Wayne
			GPIO.cleanup()												# Kill Batmans parents
			sys.exit(0)
	
	# Any main exceptions save to log.txt file:
	except Exception:
		print("Exceptoin reached???")
		GPIO.cleanup()
		sys.exit(0)
		
if __name__ == "__main__":	main()
