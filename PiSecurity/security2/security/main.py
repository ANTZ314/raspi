# -*- coding: utf-8 -*-
"""
Description:
PyImageSearch Surveillance Example edited out DropBox storage

USAGE:
python /home/pi/security/main.py --conf /home/pi/security/conf.json
"""
# import the necessary packages
from pyimagesearch.tempimage import TempImage
from picamera.array import PiRGBArray
from picamera import PiCamera
import argparse
import datetime
import imutils
import json, cv2
import warnings
import traceback
import dropbox

import time, sys, os
import btnClass as btn
import ledClass as leds
import oledClass as oled
import usbClass as usb
import RPi.GPIO as GPIO
import quitClass as quit1

path1 = "/media/pi/"													# path to USB
path2 = "/home/pi/Pictures/security/"									# path to images

####################
## SECURITY SETUP ##
####################
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--conf", required=True,
	help="path to the JSON configuration file")
args = vars(ap.parse_args())

# filter warnings, load the configuration and initialize the Dropbox client
warnings.filterwarnings("ignore")
conf = json.load(open(args["conf"]))
client = None


###################
## MAIN FUNCTION ##
###################
def main():
	## CLASS INSTANTIATION ##
	LEDS = leds.LEDClass()												# LED control class 
	USB  = usb.usbClass()												# USB Storage class
	OLED = oled.OLEDClass()												# Instantiate OLED Class
	BTN  = btn.btnClass()												# Instantiate Btn Class
	QUIT = quit1.quitClass()											# Shutdown class
	
	## FLAGS ##
	start_flg = 1														# startp menu flag
	option1   = 1														# Menu Option 1
	option2   = 1														# Menu Option 2
	confirm   = 0														# Selection flag
	quit_flg  = 0														# quit button flag
	store_flg = 0														# USB storage flag
	menu 	  = 0														# Menu display flag
	cam_resourse = 0													# camera resourse clear flag
	
	img_cnt = 0															# captured image counter
	
	LEDS.All_Off1()														# LED 1 Off
	LEDS.All_Off2()														# LED 2 Off
	print "LET'S BEGIN!!"
	
	## Any main exceptions ##
	try:
		try:
			OLED.OLEDInitialise()
			
			while True:
				##############################
				## STANDBYE MODE - CONTROLS ##
				##############################
				if BTN.switch() == 1:
					if cam_resourse == 1:
						cam_resourse = 0								# clear the flag
						camera.close()									# close the camera resourses
					
					if menu == 0:
						menu = 1
						OLED.OLEDclear()
						#print"MENU MODE"
						OLED.OLEDstore()
						
					# Show Start Menu #
					#if start_flg == 1:
					#	start_flg = 0									# only do once
					#	OLED.OLEDstore()								# Option 1
						
					if BTN.Btn1() == 1:									# Btn 1 pressed
						####################
						## Options screen ##
						####################
						if confirm == 0:								
							if option1 == 1:
								option1 = 0								# shift option
								OLED.OLEDstore()						# Option 1
								print"Store Option!!"
							else:
								option1 = 1								# shift option
								OLED.OLEDexit()							# Option 2
								print"Shutdown Option!!"
						####################
						## Confirm screen ##
						####################
						else:											
							if option1 == 0:
								if option2 == 1:						# 0/1
									option2 = 0							# shift option
									OLED.OLEDSConfirmY()				# USB Store confirm message
									print"Confirm: YES!!"
								else:
									option2 = 1							# 0/0
									OLED.OLEDSConfirmN()				# Shutdown confirmation message
									print"Confirm: NO!!"
							else:
								if option2 == 1:
									option2 = 0							# 1/1
									OLED.OLEDQConfirmY()				# USB Store confirm message
									print"Confirm: YES!!"
								else:
									option2 = 1							# 1/0
									OLED.OLEDQConfirmN()				# Shutdown confirmation message
									print"Confirm: NO!!"
						LEDS.Blink_Purple1()							# indicate btn press
						
					##############################
					## STANDBYE MODE - CONTROLS ##
					##############################
					if BTN.Btn2() == 1:
						# Selected Store or Shutdown #
						if confirm == 0:
							print"CONFRIM MODE SELECTED!!"
							confirm = not confirm						# Go to confirmation Menu
							if option1 == 0:
								OLED.OLEDSConfirmY()
							else:
								OLED.OLEDQConfirmY()
								
						# Confirmed Selection #
						else:
							print"OPTION CONFRIMED!!"
							
							# Confirm: Storage #
							if option1 == 0:
								# YES
								if option2 == 0:
									print"STORING NOW..."
									quit_flg  = 0						# quit off
									store_flg = 1						# store on
									OLED.OLEDdone()						# Completion Message
									##################################
									# Pause & Return flag to main menu
									##################################
								# NO
								else:
									print"STORAGE CANCELLED"
									OLED.OLEDcancel()					# Cancel Message
									time.sleep(2)						# pause for message
									option1 = 1							# flag to starting state
									option2 = 1							# flag to starting state
									confirm = 0							# flag to starting state
									start_flg = 1						# Back to start menu
							# Confirm: Shutdown	#	
							else:
								# YES
								if option2 == 1:
									print"SHUTDOWN CANCELLED"
									OLED.OLEDcancel()					# Cancel Message
									time.sleep(2)						# pause for message
									option1 = 1							# flag to starting state
									option2 = 1							# flag to starting state
									confirm = 0							# flag to starting state
									start_flg = 1						# Back to start menu
								# NO
								else:
									print"SHUTDOWN NOW..."
									store_flg = 0						# store off
									quit_flg = 1						# quit on
									OLED.OLEDdone()						# Change to GOODBYE!
									
						#######################
						## DATA STORE TO USB ##
						#######################
						if store_flg == 1:
							## If images folder Empty ##
							if os.listdir(path2) == []:					# pass path to USB
								print("FOLDER EMPTY")
								LEDS.Blink_Red1()						# Indicate empty folder
							else:
								## If files & USB exist, move to USB ##
								USB.usb_put(path1, path2)				# Move to USB destination
								print("Moved to USB")
							
							## Once complete -> back to stanbye mode ##
							time.sleep(2)								# pause for message
							store_flg = not store_flg					# revert storage flag
							option1 = 1									# flag to starting state
							option2 = 1									# flag to starting state
							confirm = 0									# flag to starting state
							start_flg = 1								# Back to start menu
							## Inditcate copy completion ##
							LEDS.Blink_Red1()
							LEDS.Blink_Red1()
							## Clear image counter ##
							img_cnt = 0
						else:
							LEDS.Blink_Cyan1()							# Indicate Selection
					
						######################
						## SHUTDOWN SEQUNCE ##
						######################
						if quit_flg == 1:
							LEDS.Blink_Blue2()							# indicate impending doom
							LEDS.Blink_Purple2() # Huh?
							LEDS.Blink_Blue2()							# indicate impending doom
							QUIT.quit1()								# Shutdown sequence
						
				####################################
				## ACTIVE MODE - MOTION DETECTION ##
				####################################
				else:
					if menu == 1:
						menu = 0
						OLED.OLEDclear()
						#print"CAMERA MODE"
						OLED.OLEDCapture()
						
					## Clear all flags in standby mode ##
					cam_resourse = 1									# indicate to other that camera was initialised
					option1 = 1											# 
					option2 = 1											# 
					confirm = 0											# 
					
					# check to see if the Dropbox should be used
					if conf["use_dropbox"]:
						# connect to dropbox and start the session authorization process
						client = dropbox.Dropbox(conf["dropbox_access_token"])
						print("[SUCCESS] dropbox account linked")

					# initialize the camera and grab a reference to the raw camera capture
					camera = PiCamera()
					camera.resolution = tuple(conf["resolution"])
					camera.framerate = conf["fps"]
					rawCapture = PiRGBArray(camera, size=tuple(conf["resolution"]))

					# allow the camera to warmup, then initialize the average frame, last
					# uploaded timestamp, and frame motion counter
					print("[INFO] warming up...")
					time.sleep(conf["camera_warmup_time"])
					avg = None
					lastUploaded = datetime.datetime.now()
					motionCounter = 0

					# capture frames from the camera
					for f in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
						# grab the raw NumPy array representing the image and initialize
						# the timestamp and occupied/unoccupied text
						frame = f.array
						timestamp = datetime.datetime.now()
						text = "Unoccupied"

						# resize the frame, convert it to grayscale, and blur it
						frame = imutils.resize(frame, width=500)
						gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
						gray = cv2.GaussianBlur(gray, (21, 21), 0)

						# if the average frame is None, initialize it
						if avg is None:
							print("[INFO] starting background model...")
							avg = gray.copy().astype("float")
							rawCapture.truncate(0)
							continue

						# accumulate the weighted average between the current frame and
						# previous frames, then compute the difference between the current
						# frame and running average
						cv2.accumulateWeighted(gray, avg, 0.5)
						frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(avg))

						# threshold the delta image, dilate the thresholded image to fill
						# in holes, then find contours on thresholded image
						thresh = cv2.threshold(frameDelta, conf["delta_thresh"], 255,
							cv2.THRESH_BINARY)[1]
						thresh = cv2.dilate(thresh, None, iterations=2)
						cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
							cv2.CHAIN_APPROX_SIMPLE)
						cnts = cnts[0] if imutils.is_cv2() else cnts[1]

						# loop over the contours
						for c in cnts:
							# if the contour is too small, ignore it
							if cv2.contourArea(c) < conf["min_area"]:
								continue

							# compute the bounding box for the contour, draw it on the frame,
							# and update the text
							(x, y, w, h) = cv2.boundingRect(c)
							cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
							text = "Occupied"

						# draw the text and timestamp on the frame
						ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
						cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
							cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
						cv2.putText(frame, ts, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
							0.35, (0, 0, 255), 1)

						# check to see if the room is occupied
						if text == "Occupied":
							# check to see if enough time has passed between uploads
							if (timestamp - lastUploaded).seconds >= conf["min_upload_seconds"]:
								# increment the motion counter
								motionCounter += 1

								# check to see if the number of frames with consistent motion is high enough
								if motionCounter >= conf["min_motion_frames"]:
									# check to see if dropbox sohuld be used
									if conf["use_dropbox"]:
										# write the image to temporary file
										t = TempImage()
										cv2.imwrite(t.path, frame)

										# upload the image to Dropbox and cleanup the tempory image
										print("[UPLOAD] {}".format(ts))
										path = "/{base_path}/{timestamp}.jpg".format(
											base_path=conf["dropbox_base_path"], timestamp=ts)
										client.files_upload(open(t.path, "rb").read(), path)
										t.cleanup()
									# Otherwise store image in working folder
									else:
										# Create the stored image name - Date/Time format
										#ts = timestamp.strftime("/home/pi/Pictures/security/%d-%m-%y %I_%M_%S%p") + ".jpg"
										# Create the stored image name - simple integer format
										ts = timestamp.strftime("/home/pi/Pictures/security/") + str(img_cnt) + ".jpg"
										img_cnt += 1 						# Increment the image counter
										cv2.imwrite(ts, frame)				# Store the image
										print("[SAVE] {}".format(ts))		# Feedback (can remove)
										
										# Over image storage safety
										if img_cnt == 10000:				# At 10 000 images stored
											img_cnt = 0						# Overwrite previously stored images
										
									# update the last uploaded timestamp and reset the motion counter
									lastUploaded = timestamp
									motionCounter = 0

						# otherwise, the room is not occupied
						else:
							motionCounter = 0

						# check to see if the frames should be displayed to screen
						if conf["show_video"]:
							# display the security feed
							cv2.imshow("Security Feed", frame)

						# if the `q` key is pressed, break from the loop
						key = cv2.waitKey(1) & 0xFF
						if key == ord("q"):
							#cv2.destroyAllWindows()					# release display
							once = 1									# destroy flag
							break
						# Stop button pressed, break the loop
						if BTN.Btn1() == 1:								# Btn pressed
							#cv2.destroyAllWindows()					# release display
							once = 1									# destroy flag
							break

						# clear the stream in preparation for the next frame
						rawCapture.truncate(0)
					# Wait for switch
					while BTN.switch() == 0:
						LEDS.Blink_Cyan1()
					
		# Ctrl+C will exit the program correctly:
		except KeyboardInterrupt:
			print("\r\nEXIT PROGRAM!!")									# Pistol whip Thomas Wayne
			GPIO.cleanup()												# Kill Batmans parents
			camera.close()												# save resources
			sys.exit(0)
	
	# Any main exceptions save to log.txt file:
	except Exception:
		print("Exceptoin reached")
		log = open("log.txt", 'w')
		traceback.print_exc(file=log)
		GPIO.cleanup()
		camera.close()													# save resources
		sys.exit(0)
		
if __name__ == "__main__":	main()
