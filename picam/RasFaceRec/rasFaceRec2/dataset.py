# -*- coding: utf-8 -*-
"""
Description:
Will use opencv to find & frame instances of faces being recognised, 
then use push button to manually capture training samples of 
the faces you want to train with.

Usage:
python3 face_dataset.py --cascade haarcascade_frontalface_default.xml --output dataset

Use the 'k' key to capture and the 'q' key to quit
-> Changed to button press for image capture
"""
# import the necessary packages
from imutils.video import VideoStream
import argparse
import imutils
import time
import cv2
import os
import RPi.GPIO as GPIO				# For capture button press
import ledClass as leds				# For capture indication

cascade = "haarcascade_frontalface_default.xml"
output = "dataset"

class DatasetClass:
	
	def __init__(self, **kwargs):
		print("Dataset Class init!!")

	def getPerson(self):
		Leds = leds.LEDClass()		# Create object to access 'LED' Class
		
		# Resetup capture button
		BTN = 4						# Button on pin 4
		GPIO.setmode(GPIO.BCM)		# type of GPIO
		GPIO.setup(BTN, GPIO.IN)	# set as input
		btn1 = 0					# initialise button variable
		
		# load OpenCV's Haar cascade for face detection from disk
		detector = cv2.CascadeClassifier(cascade)

		# initialize the video stream, allow the camera sensor to warm up,
		# and initialize the total number of example faces written to disk
		# thus far
		print("[INFO] starting video stream...")
		vs = VideoStream(src=0).start()					# comment out?
		#vs = VideoStream(usePiCamera=True).start()		# use this for Pi?
		time.sleep(2.0)
		total = 0

		# loop over the frames from the video stream
		while True:
			# Grab the frame from the threaded video stream, clone it, 
			# (just in case we want to write it to disk), and then 
			# resize the frame so we can apply face detection faster
			frame = vs.read()
			orig = frame.copy()
			frame = imutils.resize(frame, width=400)

			# Detect faces in the grayscale frame
			rects = detector.detectMultiScale(
				cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), scaleFactor=1.1, 
				minNeighbors=5, minSize=(30, 30))

			# Loop over the face detections and draw them on the frame
			for (x, y, w, h) in rects:
				cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
				Leds.Green_On()

			# Show the output frame
			cv2.imshow("Frame", frame)
			
			# Get key press but not wait:
			key = cv2.waitKey(1) & 0xFF		# still required for 'q' exit
			Leds.Green_Off()
			
			# Get button press instead of key:
			btn1 = GPIO.input(BTN)
			
			# If the button is pressed, write the *original* frame to disk
			# so we can later process it and use it for face recognition
			if btn1 == 1:					# push button capture
				p = os.path.sep.join([output, "{}.png".format(
					str(total).zfill(5))])
				cv2.imwrite(p, orig)
				total += 1					# increment image counter
				# Debounce btn press with LED indicator
				Leds.Quick_Red1()
				Leds.Quick_Red1()

			# If the `q` key was pressed, break from the loop
			if key == ord("q"):
				break

		# do a bit of cleanup
		print("[INFO] {} face images stored".format(total))
		print("[INFO] cleaning up...")
		# cleanup LED?
		cv2.destroyAllWindows()		# can remove if not displaying image
		vs.stop()
