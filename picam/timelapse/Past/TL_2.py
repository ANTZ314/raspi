# -*- coding: utf-8 -*-
"""
Created:		A.Smith [2017-08]
Description:	Mode test with RGB LED switch & Push Button
"""
import RPi.GPIO as GPIO
import sys, time
import picamera

# Define Pins (Using GPIO not header numbers)
GREEN 	= 18	# RGB - Green
BLUE 	= 23	# RGB - Blue
RED 	= 24	# RGB - Red
P_BTN  	= 25	# Push Button   (NC - High)
SWITCH	= 8		# Toggle Switch (NO - High)

# Use BMC GPIO Numbers:
GPIO.setmode(GPIO.BCM)

# Pin Setup:
print "Initialise Pins!"
GPIO.setup(GREEN, GPIO.OUT)	# set as output
GPIO.setup(BLUE, GPIO.OUT)	# set as output
GPIO.setup(RED, GPIO.OUT)	# set as output
GPIO.setup(P_BTN, GPIO.IN)		# External pull down
GPIO.setup(SWITCH, GPIO.IN)		# External pull up

def capture_frame(frame):
    with picamera.PiCamera() as cam:
        time.sleep(2)
        cam.capture('/home/pi/Pictures/lapse/frame%03d.jpg' % frame)

def main():
	frame = 0						# initialise image name counter
	print "LET'S BEGIN!!"
	GPIO.output(GREEN, GPIO.HIGH)	# Blue Off
	GPIO.output(BLUE, GPIO.HIGH)	# Blue Off
	GPIO.output(24, GPIO.HIGH)		# Red  Off
	print "Start-up Mode:"
	
	try:
		while True:
			# Capture Mode A
			if GPIO.input(SWITCH):					# if switch HIGH - ON
				# Capture Mode Triggered
				if GPIO.input(P_BTN):				# Btn pressed
					# Indicate capture
					GPIO.output(GREEN, GPIO.LOW)	# Green On
					GPIO.output(BLUE,  GPIO.HIGH)	# Blue Off
					GPIO.output(RED,   GPIO.HIGH)	# Red Off
					time.sleep(1)
					# Capture and image
					
					# Indicate next capture
					GPIO.output(GREEN, GPIO.HIGH)	# Green Off
					GPIO.output(BLUE,  GPIO.HIGH)	# Blue Off
					GPIO.output(RED,   GPIO.HIGH)	# Red Off
					time.sleep(1)
				
				else:
					GPIO.output(BLUE, GPIO.LOW)		# Blue On
					time.sleep(0.2)
					GPIO.output(BLUE, GPIO.HIGH)	# Blue Off
					time.sleep(0.2)
					GPIO.output(BLUE, GPIO.LOW)		# Blue On
					time.sleep(0.2)
					GPIO.output(BLUE, GPIO.HIGH)	# Blue Off
					time.sleep(0.2)
				
			# Standbye Mode A
			else:									# if switch HIGH - ON
				# Indicate stand-bye mode
				GPIO.output(GREEN, GPIO.HIGH)		# Green Off
				GPIO.output(BLUE,  GPIO.HIGH)		# Blue Off
				GPIO.output(RED,   GPIO.LOW)		# Red On
				time.sleep(2)
				# Indicate stand-bye mode
				GPIO.output(GREEN, GPIO.HIGH)		# Green Off
				GPIO.output(BLUE,  GPIO.HIGH)		# Blue Off
				GPIO.output(RED,   GPIO.HIGH)		# Red Off
				time.sleep(2)
			
	# Ctrl+C will exit the program correctly
	except KeyboardInterrupt:
		pwm.stop()			# kill Batmans parents in a dark alley
		GPIO.cleanup()		# cleanup after the crime (take Martha's pearls)
		print("\r\nEXIT PROGRAM!!")
		sys.exit(0)

if __name__ == "__main__":
	main()
