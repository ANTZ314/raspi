# -*- coding: utf-8 -*-
"""
Created:		A.Smith [2017-08]
Description:	Testing button toggling
"""
import RPi.GPIO as GPIO
import sys, time
import subprocess

# Define Pins
GREEN1 	= 2		# RGB - Green
RED1	= 3		# RGB - Blue
BLUE1 	= 4		# RGB - Red
GREEN2 	= 17	# RGB - Green
RED2  	= 27	# RGB - Blue
BLUE2	= 22	# RGB - Red
P_BTN1  = 10	# Push Button   (NC - Low)
P_BTN2  = 9		# Push Button   (NC - Low)
SWITCH	= 11	# Toggle Switch (NO - Low)

# Use BMC GPIO Numbers:
GPIO.setmode(GPIO.BCM)

# Pin Setup:
print "Initialise Pins!"
GPIO.setup(GREEN1, GPIO.OUT)	# set as output
GPIO.setup(BLUE1, GPIO.OUT)		# set as output
GPIO.setup(RED1, GPIO.OUT)		# set as output
GPIO.setup(GREEN2, GPIO.OUT)	# set as output
GPIO.setup(BLUE2, GPIO.OUT)		# set as output
GPIO.setup(RED2, GPIO.OUT)		# set as output
GPIO.setup(P_BTN1, GPIO.IN)		# External pull down
GPIO.setup(P_BTN2, GPIO.IN)		# External pull down
GPIO.setup(SWITCH, GPIO.IN)		# External pull up

def main():
	flag1 = 0
	print "LET'S BEGIN!!"
	GPIO.output(GREEN1, GPIO.LOW)	# Blue Off
	GPIO.output(BLUE1, GPIO.LOW)	# Blue Off
	GPIO.output(RED1, GPIO.LOW)		# Red  Off
	GPIO.output(GREEN2, GPIO.LOW)	# Blue Off
	GPIO.output(BLUE2, GPIO.LOW)	# Blue Off
	GPIO.output(RED2, GPIO.LOW)		# Red  Off

	try:
		while True:			
			if GPIO.input(P_BTN2) == 1:				# Not pressed (check)
				print("TRIGGER")
				flag1 = not flag1
			
			if flag1:
				GPIO.output(BLUE1, GPIO.HIGH)
				time.sleep(1)
				GPIO.output(BLUE1, GPIO.LOW)
				time.sleep(1)
				print("\r\nEXIT PROGRAM!!")			# Exit
				GPIO.cleanup()						# cleanup after the crime
				#subprocess.call("./Pwr_Bash.sh")	# run Terminal shutdown command sequence
				sys.exit(0)							# Can exit python before Bash
			else:									
				GPIO.output(GREEN1, GPIO.HIGH)
				time.sleep(1)
				GPIO.output(GREEN1, GPIO.LOW)
				time.sleep(1)
				print("*"),
	
	# Ctrl+C will exit the program correctly
	except KeyboardInterrupt:
		GPIO.cleanup()		# cleanup after the crime
		print("\r\nEXIT PROGRAM!!")
		sys.exit(0)

if __name__ == "__main__":
	main()
