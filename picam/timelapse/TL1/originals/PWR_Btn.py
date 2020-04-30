# -*- coding: utf-8 -*-
"""
Created:		A.Smith [2017-08]
Description:	Testing button toggling
"""
import RPi.GPIO as GPIO
import sys, time
import subprocess

# Define Pins
BLUE 	= 23			# Blue
P_BTN  	= 25			# Button
GREEN 	= 18			# guess

# Use BMC GPIO Numbers:
GPIO.setmode(GPIO.BCM)

# Pin Setup:
print "Initialise Pins!"
GPIO.setup(BLUE, GPIO.OUT)		# set as output
GPIO.setup(GREEN, GPIO.OUT)		# set as output
GPIO.setup(P_BTN, GPIO.IN)		# already have pull down

def main():
	flag1 = 0
	print "Start loop!"
	GPIO.output(BLUE, GPIO.HIGH)	# Off
	GPIO.output(GREEN, GPIO.HIGH)	# Off

	try:
		while True:			
			if GPIO.input(P_BTN) == 0:		# Not pressed (check)
				print("TRIGGER")
				flag1 = not flag1
			
			if flag1:
				GPIO.output(BLUE, GPIO.LOW)
				time.sleep(1)
				GPIO.output(BLUE, GPIO.HIGH)
				time.sleep(1)
				print("\r\nEXIT PROGRAM!!")			# Exit
				GPIO.cleanup()						# cleanup after the crime
				subprocess.call("./Pwr_Bash.sh")	# run Terminal shutdown command sequence
				sys.exit(0)							# Can exit python before Bash
			else:									
				GPIO.output(GREEN, GPIO.LOW)
				time.sleep(1)
				GPIO.output(GREEN, GPIO.HIGH)
				time.sleep(1)
				print("*"),
	
	# Ctrl+C will exit the program correctly
	except KeyboardInterrupt:
		GPIO.cleanup()		# cleanup after the crime
		print("\r\nEXIT PROGRAM!!")
		sys.exit(0)

if __name__ == "__main__":
	main()
