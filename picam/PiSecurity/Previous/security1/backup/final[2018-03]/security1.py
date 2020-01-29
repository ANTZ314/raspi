# -*- coding: utf-8 -*-
"""
Description:
PyImageSearch Surveillance Example edited out DropBox storage

USAGE:
$ python security1.py --conf conf1.json
"""
# import the necessary packages
from pyimagesearch.tempimage import TempImage
from picamera.array import PiRGBArray
from picamera import PiCamera
import argparse
import warnings
import datetime
import dropbox
import imutils
import json
import time, sys, os
import cv2
import ledClass as leds
import btnClass as btn
import usbClass as usb
import quitClass as quit1
import RPi.GPIO as GPIO

path1 = "/media/pi/"													# path to USB
path2 = "/home/pi/Pictures/dropbox/"									# path to images

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
	quit_flg  = 0														# quit button flag
	store_flg = 0														# USB storage flag
	confirm   = 0														# quit confirmation
	quit_conf = 0														# 2nd quit confirmation
	once      = 0														# exit video mode flag
	
	LEDS = leds.LEDClass()												# LED control class 
	BTN  = btn.btnClass()												# Push Btn class
	USB  = usb.usbClass()												# USB Storage class
	QUIT = quit1.quitClass()											# Shutdown class
	
	LEDS.All_Off1()														# LED 1 Off
	LEDS.All_Off2()														# LED 2 Off
	print "LET'S BEGIN!!"
	try:
		while True:
			##############################
			## STANDBYE MODE - CONTROLS ##
			##############################
			if BTN.switch():											# if switch HIGH - ON
				# kill video feed properly once
				if once == 1:
					once = 0											# re-clear flag
					cv2.destroyAllWindows()								# kill cv2 windows
					LEDS.Blink_Green1()									# quick indicator
										
				################
				## STORE BTN: ##
				################	
				if BTN.Btn1() == 1:										# Btn pressed
					print("STORE IMAGES TO USB!")
					for x in range(0, 3):
						LEDS.Quick_Blue1()								# Blink 3 times: indicator
					# Toggle Button Press
					quit_flg  = 0										# confirm off
					store_flg = not store_flg							# toggle flag
				
				###############
				## QUIT BTN: ##
				###############
				if BTN.Btn2() == 1:
					print("EXIT BUTTON!")
					for x in range(0, 3):
						LEDS.Quick_Blue1()								# Blink 3 times: indicator
					# Toggle Button Press
					quit_flg  = not quit_flg							# set flag
					store_flg = 0										# confirm off
					
				#######################
				## DATA STORE TO USB ##
				#######################
				if store_flg == 1:
					LEDS.Blink_Red1()
					## If images folder Empty ##
					if os.listdir(path2) == []:							# pass path to USB
						print("FOLDER EMPTY")
						LEDS.Blink_Red1()								# Indicate empty folder
					else:
						## If files & USB destination exists, move to USB ##
						USB.usb_put(path1, path2)						# Move to USB destination
						print("Moved to USB")
						exit_flag = 1
					
					# Once complete -> back to stanbye mode
					time.sleep(2)
					store_flg = not store_flg
				else:
					if quit_flg == 0:
						# Blink Violet to indicate standbye mode
						LEDS.Blink_Purple1()
					
				##############
				## SHUTDOWN ##
				##############
				if quit_flg == 1:					
					# Quit confirmed (button pressed again)
					while quit_conf < 5:
						# Blink Yellow until confirmed quit
						LEDS.Blink_Yellow1()
						if BTN.Btn2() == 1:
							for x in range(0, 3):
								LEDS.Quick_Blue1()
							confirm = 1
							break
						quit_conf += 1									# increment counter
						#time.sleep(1)									# 1 sec wait
						
					# Quit was confirmed in 10 sec
					if confirm == 1:
						LEDS.Blink_Green1()
						quit_conf = 0									# clear value
						confirm = 0										# clear value
						# Shutdown sequence
						QUIT.quit1()
						# Temporary
						GPIO.cleanup()									# Kill Batmans parents
						sys.exit(0)										# Take Martha's pearls
		
					# Otherwise return to standbye mode
					else:
						quit_conf = 0									# clear value
						confirm = 0										# clear value
						quit_flg = 0									# set flag
						store_flg = 0									# confirm off
					
			####################################
			## ACTIVE MODE - MOTION DETECTION ##
			####################################
			else:														# if switch HIGH - ON
				once = 0												# clear once flag
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

							# check to see if the number of frames with consistent motion is
							# high enough
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
									# Create the stored image name
									ts = timestamp.strftime("/home/pi/Pictures/dropbox/%d-%m-%y %I_%M_%S%p") + ".jpg"
									cv2.imwrite(ts, frame)				# Store the image
									# Feed back (can remove)
									print("[SAVE] {}".format(ts))
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
					
	# Ctrl+C will exit the program correctly
	except KeyboardInterrupt:
		print("\r\nEXIT PROGRAM!!")										# Pistol whip Thomas Wayne
		GPIO.cleanup()													# Kill Batmans parents
		sys.exit(0)														# Take Martha's pearls

if __name__ == "__main__":	main()
