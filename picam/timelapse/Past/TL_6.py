# -*- coding: utf-8 -*-
"""
Created:		A.Smith [2017-08]
Description:	Mode test with RGB LED switch & Push Button [optimised code V01]
"""
import OLEDtext as OLED
import RPi.GPIO as GPIO
import sys, time
import picamera

# Define Pins (Using GPIO not header numbers)
GREEN1 	= 2		# RGB - Green
BLUE1 	= 3		# RGB - Blue
RED1 	= 4		# RGB - Red
GREEN2 	= 17	# RGB - Green
BLUE2 	= 27	# RGB - Blue
RED2 	= 22	# RGB - Red
#P_BTN1  = 10	# Push Button   (NC - Low)
#P_BTN2  = 9		# Push Button   (NC - Low)
#SWITCH	= 11	# Toggle Switch (NO - Low)

# Use BMC GPIO Numbers:
GPIO.setmode(GPIO.BCM)

# Pin Setup:
print "Initialise Pins!"
GPIO.setup(GREEN1, GPIO.OUT)		# set as output
GPIO.setup(BLUE1, GPIO.OUT)		# set as output
GPIO.setup(RED1, GPIO.OUT)		# set as output
GPIO.setup(GREEN2, GPIO.OUT)		# set as output
GPIO.setup(BLUE2, GPIO.OUT)		# set as output
GPIO.setup(RED2, GPIO.OUT)		# set as output
#GPIO.setup(P_BTN1, GPIO.IN)		# External pull down
#GPIO.setup(P_BTN2, GPIO.IN)		# External pull down
#GPIO.setup(SWITCH, GPIO.IN)		# External pull up

# List of Interval Strings 10sec, 30sec, 1min, 10min
inters = ["10sec", "30sec", "1min", "10min"]

# List of duration strings 10min, 30min, 1Hr, 6Hr
durs = ["5min", "10min", "30min", "1Hour"]

def capture_frame(frame):
    with picamera.PiCamera() as cam:
        time.sleep(2)
        cam.capture('/home/pi/Pictures/lapse/frame%03d.jpg' % frame)

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
	option = 0						# scroll through 4 options
	key = 0							# key press
	
	oled = OLED.OLEDtext()			# create class object
	
	print "LET'S BEGIN!!"
	"""
	GPIO.output(GREEN1, GPIO.LOW)	# Blue Off
	GPIO.output(BLUE1, GPIO.LOW)	# Blue Off
	GPIO.output(RED1, GPIO.LOW)		# Red  Off
	GPIO.output(GREEN2, GPIO.LOW)	# Blue Off
	GPIO.output(BLUE2, GPIO.LOW)	# Blue Off
	GPIO.output(RED2, GPIO.LOW)		# Red  Off
	"""
	print "Start-up Mode:"
	durations = 555
	intervals = 737
	
	try:
		oled.clear_oled()
		oled.draw(intervals, durations)
		time.sleep(3)
		
		"""
		NOTE:
		* check actual values, interval can never be more than duration
		* if interval is not divisible by duration?
		* check for select button to scroll values
		* Enter button moves between "interval" & "duration"
		* long press to start - indicated with RGB (only need one now)
		"""
		
		
		while True:
			if key == 3:
				key = 0								# temporary key press
				# 10sec, 30sec, 1min, 10min
				if option < 4:
					intervals = inters[option]		# get new interval string
					# get actual interval value
					durations = durs[option]		# get new duration
					# get actual duration value
					option += 1						# increment to next option
				else:
					option = 0						# reset option counter
								
				oled.clr_Space()					# clear old values from OLED
				time.sleep(0.25)
				oled.draw(intervals, durations)		# update new values to OLED
			else:
				print "*",
				key += 1
				time.sleep(2)
			
	# Ctrl+C will exit the program correctly
	except KeyboardInterrupt:
		print("\r\nEXIT PROGRAM!!")
		GPIO.cleanup()								# Kill Batmans parents
		sys.exit(0)									# Take Martha's pearls

if __name__ == "__main__":
	main()
