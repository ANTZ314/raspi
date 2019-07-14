#!/usr/bin/env python
"""
# -*- coding: utf-8 -*-
Description:
PyImageSearch Surveillance Example edited out DropBox storage

USAGE:
$ python security1.py --conf conf1.json
"""
# import the necessary packages
import gaugette.ssd1306
import gaugette.platform
import gaugette.gpio
import datetime
import dropbox
import imutils
import time, sys, os
import ledClass as leds
import btnClass as btn
import RPi.GPIO as GPIO

####################
## SECURITY SETUP ##
####################

###################
## MAIN FUNCTION ##
###################
def main():
	
	LEDS = leds.LEDClass()												# LED control class 
	BTN  = btn.btnClass()												# Push Btn class
	
	LEDS.All_Off1()														# LED 1 Off
	LEDS.All_Off2()														# LED 2 Off
	print "LET'S BEGIN!!"
	
	# Any main exceptions:
	try:
		# Ctl+C early quit key
		try:
			while True:
				##############################
				## STANDBYE MODE - CONTROLS ##
				##############################
				if BTN.switch():											# if switch HIGH - ON
					LEDS.Blink_Green1()									# quick indicator
											
					################
					## STORE BTN: ##
					################	
					if BTN.Btn1() == 1:										# Btn pressed
						for x in range(0, 3):
							LEDS.Quick_Blue1()								# Blink 3 times: indicator
					
					###############
					## QUIT BTN: ##
					###############
					if BTN.Btn2() == 1:
						for x in range(0, 3):
						LEDS.Blink_Purple1()
						
					##############
					## SHUTDOWN ##
					##############
					LEDS.Blink_Yellow1()
							
						
				####################################
				## ACTIVE MODE - MOTION DETECTION ##
				####################################
				else:														# if switch HIGH - ON
					# Wait for switch
					while BTN.switch() == 0:
						LEDS.Blink_Cyan1()
						
		# Ctrl+C will exit the program correctly:
		except KeyboardInterrupt:
			print("\r\nEXIT PROGRAM!!")										# Pistol whip Thomas Wayne
			GPIO.cleanup()													# Kill Batmans parents
			sys.exit(0)														# Take Martha's pearls
	
	# Any main exceptions save to log.txt file:
	except Exception:
		print("Exceptoin reached")
		log = open("log.txt", 'w')
		traceback.print_exc(file=log)
		GPIO.cleanup()
		sys.exit(0)
		
if __name__ == "__main__":	main()
