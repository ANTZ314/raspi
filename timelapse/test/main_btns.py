# -*- coding: utf-8 -*-
"""
Created:		A.Smith [2017-08]
Description:	Test individual classes
"""
import ledClass as leds
import btnClass as btn
import RPi.GPIO as GPIO
import sys, time

"""
P_BTN1  = 9  #10						# Push Button   (NC - Low)
P_BTN2  = 10 #5							# Push Button   (NC - Low)
SWITCH	= 11 #6							# Toggle Switch (NO - Low)


GPIO.setmode(GPIO.BCM)					# 
GPIO.setup(P_BTN1, GPIO.IN)				# External pull down
GPIO.setup(P_BTN2, GPIO.IN)				# External pull down
GPIO.setup(SWITCH, GPIO.IN)				# External pull up
"""
#################
# MAIN FUNCTION #
#################
def main():
	LEDS = leds.LEDClass()							# LED control class 
	BTN  = btn.btnClass()							# Push Btn class
	
	print "LET'S BEGIN!!"
	LEDS.All_Off1()									# LED 1 Off
	LEDS.All_Off2()									# LED 2 Off
	print "Start-up Mode:"
	
	try:
		while True:
			if BTN.switch() == 1:
				LEDS.Blink_GR2()
			elif BTN.Btn1() == 1:
				LEDS.Blink_GB2()
			elif BTN.Btn2() == 1:
				LEDS.Blink_BR2()
			else:		
				LEDS.Blink_Green1()
			
			
	# Ctrl+C will exit the program correctly
	except KeyboardInterrupt:
		print("\r\nEXIT PROGRAM!!")					# Pistol whip Thomas Wayne
		GPIO.cleanup()								# Kill Batmans parents
		sys.exit(0)									# Take Martha's pearls

if __name__ == "__main__":	main()
