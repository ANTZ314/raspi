# -*- coding: utf-8 -*-
"""
Created:		A.Smith [2017-11]
Description:	Main Time Lapse File calling functional Classes

Functionality:	
"""
import ledClass as leds
import RPi.GPIO as GPIO
import usbClass as usb
import RPi.GPIO as GPIO
import sys, time
import picamera

## RASPI VERSION ##
#path1 = "/media/pi/"													# Destination Media path on USB
#path2 = "/home/pi/Pictures/4.jpg"										# Source path for converting/converted mp4 file
#path3 = "/home/pi/Pictures/lapse/frame%03d.jpg"						# Destination path for time lapse images
## UBUNTU VERSION ##
path1 = "/home/antz/Pictures/4.jpg"										# Source path for converting/converted mp4 file
path2 = "/media/antz/"													# Destination Media path on USB
path3 = "/home/antz/Pictures/lapse/frame%03d.jpg"						# Destination path for time lapse images

################
## GPIO STUFF ##
################
P_BTN1  = 10	# Push Button   (NC - Low)
P_BTN2  = 9		# Push Button   (NC - Low)
SWITCH	= 11	# Toggle Switch (NO - Low)

GPIO.setup(P_BTN1, GPIO.IN)		# External pull down
GPIO.setup(P_BTN2, GPIO.IN)		# External pull down
GPIO.setup(SWITCH, GPIO.IN)		# External pull up

#########################
## TIMELAPSE CAPTURING ##
#########################
def capture_frame(frame):
    with picamera.PiCamera() as cam:
        time.sleep(2)
        #cam.capture('/home/pi/Pictures/lapse/frame%03d.jpg' % frame)
        cam.capture(str(path3) % frame)									# attempt cleanup?

#########################################
## VARIABLE PAUSE BTWN CAPTURED FRAMES ##
#########################################
def capture_wait(check, pause):			
	if check == True:
		for x in range (int(pause)):
			time.sleep(1)		
	else:
		print("Incorrect value!")

#################
# MAIN FUNCTION #
#################
def main():
	LEDS = leds.LEDClass()												# create class instance
	USB = usb.usbClass()												# create class instance
	
	frame_cnt = 0														# initialise frame counter
	frame = 0															# initialise image name counter
	once1 = 0															# Capture Mode
	cap_flg = 0															# Capture flag
	print "LET'S BEGIN!!"
	LEDS.All_Off1()														# LED 1 Off
	LEDS.All_Off2()														# LED 2 Off
	print "Start-up Mode:"
	
	try:
		while True:
			##################
			## Capture Mode ##
			##################
			if GPIO.input(SWITCH):										# if switch HIGH - ON
				if once1 == 1:
					print("Capture Mode!")								# Display mode
					once1 = not once1									# Toggle flag
					
				if GPIO.input(P_BTN1) == 1:								# Btn pressed
					print("CAPTURE MODE TRIGGER!")
					for x in range(0, 3):
						LEDS.Quick_Blue1()								# Blink 3 times: indicator
					# Toggle between Capture and Pause Modes
					cap_flg = not cap_flg								# toggle flags mode
					# Select Capture Pause Duration
					if cap_flg:
						pause = raw_input("Pause between frames: ")		# Pause time (+2sec for capture)
						check1 = pause.isdigit()						# Is input value an integer
						frames = raw_input("No of Frames: ")			# Number of frames to capture
						check2 = frames.isdigit()						# Is input value an integer
						if check1 == False & check2 == False:			# if frames is an integer
							print("one of the valuse given is incorrect")
							cap_flg = not cap_flg						# Go back to 'Wait Mode'
						else:
							print("both values Okay - start capturing")
							
				##############################
				## Capture Mode B - Capture ##
				##############################
				if cap_flg:
					## loop until number of frames reached ##
					if frame_cnt < int(frames):							# use values like [frame-1]
						print("Capturing!!")							# remove
						## Capture single image ##
						#capture_frame(frame_cnt)	# +2sec				# capture & increment name.jpg
						frame_cnt += 1									# increment frmae counter
						LEDS.Blink_Blue1()				# +1sec			# Blink once on each capture
						## Compensate for capture time ##
						pause = int(pause)
						if pause > 2:
							pause = pause - 2
						## Pause for 'pause' length of time ##
						capture_wait(check1, pause)						#(+2sec capture + 1.5sec LED blink)
					## frames reached exit capture ##
					else:
						print("Complete! - Standby")
						cap_flg = not cap_flg							# toggle capture mode to wait
					
				############################
				## Capture Mode A - Pause ##
				############################
				else:
					LEDS.Blink_Green1()									# Waiting for Trigger (indicator)
			
			###################
			## Standbye Mode ##
			###################
			else:														# if switch HIGH - ON
				if once1 == 0:
					print("Standby Mode!")								# Display mode
					once1 = not once1									# Toggle flag
				
				#################################
				## Compile, Save to USB & Exit ##
				#################################
				if GPIO.input(P_BTN1) == 1:								# Btn pressed
					for x in range(0, 3):
						LEDS.Quick_Blue1()
					# If images in folder
					print("Saving to Video...")							# Save to and compile
					## Bash file to Compile to MP4 ##
					
					## If file exists & USB dest, move to destination ##
					USB.usb_put(path2)				
					time.sleep(2)										# delay before Exit
					
					## Clean up RasPi GPIOs ##
					print("\r\nEXIT PROGRAM!!")
					GPIO.cleanup()										# Kill Batmans parents
					## Shutdown Bash file ##
					sys.exit(0)											# Take Martha's pearls
					
				###################
				## Standbye Wait ##
				###################
				else:											# Wait Mode
					LEDS.Blink_Red1()
			
	# Ctrl+C will exit the program correctly
	except KeyboardInterrupt:
		print("\r\nEXIT PROGRAM!!")								# Pistol whip Thomas Wayne
		GPIO.cleanup()											# Kill Batmans parents
		sys.exit(0)												# Take Martha's pearls

if __name__ == "__main__":
	main()
