# -*- coding: utf-8 -*-
"""
Description: 
Test blink LED
"""
import RPi.GPIO as GPIO 		## Import GPIO library
import time 					## Import 'time' library. Allows us to use 'sleep'
import sys

LED = 14

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED, GPIO.OUT) 		## Setup GPIO Pin 2 to OUT


##Define a function named Blink()
def BlinkLed(numTimes,speed):	
	for i in range(0,numTimes):	## Run loop numTimes
		GPIO.output(LED,True)	## Switch on pin 7
		time.sleep(speed)		## Wait
		GPIO.output(LED,False)	## Switch off pin 7
		time.sleep(speed)		## Wait
	print "LED..."

def main():
	toggle = False
	iterations = 2
	speed = 1
	
	try:
		while True:
			BlinkLed(int(iterations),float(speed))
			print("toggle: " + str(toggle))

	# Ctrl+C will exit the program correctly
	except KeyboardInterrupt:
		print("\r\nEXIT PROGRAM!!")					# Pistol whip Thomas Wayne
		GPIO.cleanup()								# spit on Bruce
		sys.exit(0)									# Take Martha's pearls

if __name__ == "__main__":	main()
