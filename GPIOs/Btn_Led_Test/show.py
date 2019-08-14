# -*- coding: utf-8 -*-
"""
Description: 

"""
import RPi.GPIO as GPIO 		## Import GPIO library
import time 					## Import 'time' library
import sys
import numpy as np
import cv2

RED = 2
GRN = 3
BTN = 4
speed = 100

#GPIO.setmode(GPIO.BOARD) 		## Use board pin numbering
GPIO.setmode(GPIO.BCM)
GPIO.setup(RED, GPIO.OUT) 		## Setup GPIO Pin 2 to OUT
GPIO.setup(GRN, GPIO.OUT) 		## Setup GPIO Pin 3 to OUT
GPIO.setup(BTN, GPIO.IN) 		## Setup GPIO Pin 4 to OUT


##Define a function named Blink()
def BlinkRd(numTimes,speed):
	GPIO.output(GRN,True)				## Switch off pin 7
	
	for i in range(0,numTimes):			## Run loop numTimes
		#print "Iteration " + str(i+1) 	## Print current loop
		GPIO.output(RED,False)			## Switch on pin 7
		time.sleep(speed)				## Wait
		GPIO.output(RED,True)			## Switch off pin 7
		time.sleep(speed)					## Wait
	print ("RED...")

##Define a function named Blink()
def BlinkGr(numTimes,speed):
	GPIO.output(RED,True)				## Switch off pin 7
	
	for i in range(0,numTimes):			## Run loop numTimes
		#print "Iteration " + str(i+1) 	## Print current loop
		GPIO.output(GRN,False)			## Switch on pin 7
		time.sleep(speed)				## Wait
		GPIO.output(GRN,True)			## Switch off pin 7
		time.sleep(speed)				## Wait
	print ("GREEN...")

def main():
	try:
		image = cv2.imread('/home/pi/Pictures/00001.jpg')
	
		# Show the output image:
		cv2.imshow("Image", image)
		cv2.waitKey(0)
		cv2.destroyAllWindows()
		BlinkRd(3,0.5)					# (repeat, seconds)
		GPIO.cleanup()	
		print("DONE!!")

	# Ctrl+C will exit the program correctly
	except KeyboardInterrupt:
		print("EXIT!!")
		#cv2.destroyAllWindows()
		GPIO.cleanup()								# spit on Bruce
		sys.exit(0)									# Take Martha's pearls

if __name__ == "__main__":	main()
