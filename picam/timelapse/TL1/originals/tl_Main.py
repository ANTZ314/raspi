# -*- coding: utf-8 -*-
"""
Created:		A.Smith [2017-08]
Description:	Mode test with RGB LED switch & Push Button [optimised code V01]
"""
import RPi.GPIO as GPIO
import sys, time
import picamera

# Define Pins (Using GPIO not header numbers)
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

def capture_frame(frame):
    with picamera.PiCamera() as cam:
        time.sleep(2)
        cam.capture('/home/pi/Pictures/lapse/frame%03d.jpg' % frame)

def capture_wait(check, pause):			
	if check == True:
		for x in range (int(pause)):
			time.sleep(1)		
	else:
		print("Incorrect value!")

def Blink_Blue():
	# All Off
	GPIO.output(GREEN1, GPIO.LOW)	# Green Off
	GPIO.output(BLUE1,  GPIO.LOW)	# Blue Off
	GPIO.output(RED1,   GPIO.LOW)	# Red Off
	GPIO.output(GREEN2, GPIO.LOW)	# Green Off
	GPIO.output(BLUE2,  GPIO.LOW)	# Blue Off
	GPIO.output(RED2,   GPIO.LOW)	# Red Off
	# Blink
	GPIO.output(BLUE1,  GPIO.HIGH)	# Blue On
	time.sleep(0.2)
	GPIO.output(BLUE1,  GPIO.LOW)	# Blue Off
	time.sleep(0.2)
	GPIO.output(BLUE2,  GPIO.HIGH)	# Blue On
	time.sleep(0.2)
	GPIO.output(BLUE2,  GPIO.LOW)	# Blue Off
	time.sleep(0.2)

def Blink_Red():
	# All Off
	GPIO.output(GREEN1, GPIO.LOW)	# Green Off
	GPIO.output(BLUE1,  GPIO.LOW)	# Blue Off
	GPIO.output(RED1,   GPIO.LOW)	# Red Off
	GPIO.output(GREEN2, GPIO.LOW)	# Green Off
	GPIO.output(BLUE2,  GPIO.LOW)	# Blue Off
	GPIO.output(RED2,   GPIO.LOW)	# Red Off
	# Blink
	GPIO.output(RED1,   GPIO.HIGH)	# Red On
	time.sleep(0.5)
	GPIO.output(RED1,   GPIO.LOW)	# Red Off
	time.sleep(0.2)
	GPIO.output(RED2,   GPIO.HIGH)	# Red On
	time.sleep(0.5)
	GPIO.output(RED2,   GPIO.LOW)	# Red Off
	time.sleep(2)

def Blink_Green():
	# All Off
	GPIO.output(GREEN1, GPIO.LOW)	# Green Off
	GPIO.output(BLUE1,  GPIO.LOW)	# Blue Off
	GPIO.output(RED1,   GPIO.LOW)	# Red Off
	GPIO.output(GREEN2, GPIO.LOW)	# Green Off
	GPIO.output(BLUE2,  GPIO.LOW)	# Blue Off
	GPIO.output(RED2,   GPIO.LOW)	# Red Off
	# Blink
	GPIO.output(GREEN1, GPIO.HIGH)	# Green On
	time.sleep(0.5)
	GPIO.output(GREEN1, GPIO.LOW)	# Green Off
	time.sleep(0.2)
	GPIO.output(GREEN2, GPIO.HIGH)	# Green On
	time.sleep(0.5)
	GPIO.output(GREEN2, GPIO.LOW)	# Green Off
	time.sleep(2)

#################
# MAIN FUNCTION #
#################
def main():
	frame = 0						# initialise image name counter
	once1 = 0						# Capture Mode
	cap_flg = 0						# Capture flag
	print "LET'S BEGIN!!"
	GPIO.output(GREEN1, GPIO.LOW)	# Blue Off
	GPIO.output(BLUE1, GPIO.LOW)	# Blue Off
	GPIO.output(RED1, GPIO.LOW)		# Red  Off
	GPIO.output(GREEN2, GPIO.LOW)	# Blue Off
	GPIO.output(BLUE2, GPIO.LOW)	# Blue Off
	GPIO.output(RED2, GPIO.LOW)		# Red  Off
	print "Start-up Mode:"
	
	try:
		while True:
			# Capture Mode A
			if GPIO.input(SWITCH):					# if switch HIGH - ON
				if once1 == 1:
					print("Capture Mode!")			# Display mode
					once1 = not once1				# Toggle flag
					
				# Capture Mode B
				if GPIO.input(P_BTN1) == 1:			# Btn pressed
					print("CAPTURE MODE CHANGE!")
					for x in range(0, 3):
						Blink_Blue()				# Blink 3 times: indicator
					# Start Capturing!!
					cap_flg = not cap_flg			# toggle flags mode
					# Select Capture Pause Duration
					if cap_flg:
						pause = raw_input("Pause 1 - 5: ")
						check = pause.isdigit()
					
				if cap_flg:
					print("Capturing!!")
					Blink_Blue()					# Blink once on each capture
					capture_wait(check, pause)					
					
				# Waiting Capture Trigger	
				else:
					Blink_Green()
				
			# Standbye Mode A
			else:									# if switch HIGH - ON
				if once1 == 0:
					print("Standby Mode!")			# Display mode
					once1 = not once1				# Toggle flag
					
				# Exit
				if GPIO.input(P_BTN1) == 1:			# Btn pressed
					for x in range(0, 2):
						Blink_Blue()
					# If images in folder
					print("Saving to Video...")		# Save to and compile
					time.sleep(2)					# delay before Exit
					# Then EXIT (or return to standby)
					print("\r\nEXIT PROGRAM!!")
					GPIO.cleanup()					# Kill Batmans parents
					sys.exit(0)						# Take Martha's pearls
					
				else:								# Wait Mode
					Blink_Red()
			
	# Ctrl+C will exit the program correctly
	except KeyboardInterrupt:
		print("\r\nEXIT PROGRAM!!")
		GPIO.cleanup()								# Kill Batmans parents
		sys.exit(0)									# Take Martha's pearls

if __name__ == "__main__":
	main()
