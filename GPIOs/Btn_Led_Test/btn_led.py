# -*- coding: utf-8 -*-
"""
Description: 

"""
import RPi.GPIO as GPIO 		## Import GPIO library
import time 					## Import 'time' library. Allows us to use 'sleep'
import sys

RED = 2
GRN = 3
BTN = 4

#GPIO.setmode(GPIO.BOARD) 		## Use board pin numbering
GPIO.setmode(GPIO.BCM)
GPIO.setup(RED, GPIO.OUT) 		## Setup GPIO Pin 2 to OUT
GPIO.setup(GRN, GPIO.OUT) 		## Setup GPIO Pin 3 to OUT
GPIO.setup(BTN, GPIO.IN) 		## Setup GPIO Pin 4 to OUT


##Define a function named Blink()
def BlinkRd(numTimes,speed):
	GPIO.output(GRN,True)	## Switch off pin 7
	
	for i in range(0,numTimes):	## Run loop numTimes
		#print "Iteration " + str(i+1) ## Print current loop
		GPIO.output(RED,True)		## Switch on pin 7
		time.sleep(speed)		## Wait
		GPIO.output(RED,False)	## Switch off pin 7
		time.sleep(speed)		## Wait
	print "RED..."

##Define a function named Blink()
def BlinkGr(numTimes,speed):
	GPIO.output(RED,True)	## Switch off pin 7
	
	for i in range(0,numTimes):	## Run loop numTimes
		#print "Iteration " + str(i+1) ## Print current loop
		GPIO.output(GRN,True)		## Switch on pin 7
		time.sleep(speed)		## Wait
		GPIO.output(GRN,False)	## Switch off pin 7
		time.sleep(speed)		## Wait
	print "GREEN..."

def main():
	toggle = False
	btn1 = 0
	iterations = 2
	speed = 1
	
	try:
		while True:
			btn1 = GPIO.input(BTN)

			## toggle on each button press
			if btn1 == 1:
				toggle = not toggle
				
			if toggle == True:
				BlinkRd(int(iterations),float(speed))
				print("toggle: " + str(toggle))
			else:
				BlinkGr(int(iterations),float(speed))
				print("toggle: " + str(toggle))

	# Ctrl+C will exit the program correctly
	except KeyboardInterrupt:
		print("\r\nEXIT PROGRAM!!")					# Pistol whip Thomas Wayne
		GPIO.cleanup()								# spit on Bruce
		sys.exit(0)									# Take Martha's pearls

if __name__ == "__main__":	main()
