#!/usr/bin/env python
"""
# -*- coding: utf-8 -*-
Description:
OLED class Tester script

USAGE:
$ python oled2.py
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
	## CLASS INSTANTIATION ##
	LEDS = leds.LEDClass()												# LED control class 
	OLED = oled.OLEDClass()												# Instantiate OLED Class
	BTN  = btn.btnClass()												# Instantiate Btn Class
	
	## FLAGS ##
	option1 = 1
	option2 = 1
	confirm = 0
	menu 	= 0
	
	LEDS.All_Off1()														# LED 1 Off
	LEDS.All_Off2()														# LED 2 Off
	print "LET'S BEGIN!!"
	
	## Any main exceptions ##
	try:
		try:
			OLED.OLEDInitialise()
			
			while True:
				##############################
				## STANDBYE MODE - CONTROLS ##
				##############################
				if BTN.switch() == 1:
					if menu == 0:
						menu = 1
						OLED.OLEDclear()
						print"MENU MODE"
						OLED.OLEDstore()
					
					##############################
					## STANDBYE MODE - CONTROLS ##
					##############################
					if BTN.Btn1() == 1:									# Btn 1 pressed							
						## Options screen ##
						if confirm == 0:								
							if option1 == 1:
								option1 = 0								# shift option
								OLED.OLEDstore()						# Option 1
								print"Store Option!!"
							else:
								option1 = 1								# shift option
								OLED.OLEDexit()							# Option 2
								print"Shutdown Option!!"
						
						## Confirm screen ##
						else:											
							if option1 == 0:
								if option2 == 1:						# 0/1
									option2 = 0							# shift option
									OLED.OLEDSConfirmY()				# USB Store confirm message
									print"Confirm: YES!!"
								else:
									option2 = 1							# 0/0
									OLED.OLEDSConfirmN()				# Shutdown confirmation message
									print"Confirm: NO!!"
							else:
								if option2 == 1:
									option2 = 0							# 1/1
									OLED.OLEDQConfirmY()				# USB Store confirm message
									print"Confirm: YES!!"
								else:
									option2 = 1							# 1/0
									OLED.OLEDQConfirmN()				# Shutdown confirmation message
									print"Confirm: NO!!"
									
						LEDS.Blink_Purple1()							# indicate btn press
						
					##############################
					## STANDBYE MODE - CONTROLS ##
					##############################
					if BTN.Btn2() == 1:
						# Selected Store or Shutdown
						if confirm == 0:
							print"CONFRIM MODE SELECTED!!"
							confirm = not confirm						# Go to confirmation Menu
							if option1 == 0:
								OLED.OLEDSConfirmY()
							else:
								OLED.OLEDQConfirmY()
								
						# Confirmed Selection
						else:
							print"OPTION CONFRIMED!!"
							# Confirm: Storage
							if option1 == 0:
								# YES
								if option2 == 0:
									print"STORING NOW..."
									OLED.OLEDdone()						# Completion Message
								# NO
								else:
									print"STORAGE CANCELLED"
									OLED.OLEDcancel()
									
							# Confirm: Shutdown		
							else:
								# YES
								if option2 == 0:
									print"SHUTDOWN NOW..."
									OLED.OLEDdone()						# Completion Message
								# NO
								else:
									print"SHUTDOWN CANCELLED"
									OLED.OLEDcancel()
							
						LEDS.Blink_Cyan1()								# Indicate Selection
					
				####################################
				## ACTIVE MODE - MOTION DETECTION ##
				####################################
				else:
					if menu == 1:
						menu = 0
						OLED.OLEDclear()
						print"CAMERA MODE"
						OLED.OLEDCapture()
					
					## Clear all flags in standby mode ##
					option1 = 1
					option2 = 1
					confirm = 0
					
					LEDS.Blink_Red2()									# Indicate Capturing

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
