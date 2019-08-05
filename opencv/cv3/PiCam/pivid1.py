# -*- coding: utf-8 -*-
"""
Make sure installed:
pip install "picamera[array]

Description: 
Opens the camera module and displays each frame
"q" to quit

Run:
$ python pivid1.py test2.mp4
"""
# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

def main(): 
	# initialize the camera and grab a reference to the raw camera capture
	camera = PiCamera()
	camera.resolution = (640, 480)						# set the image resolution	  (max = ?)
	camera.brightness = 70								# increase default brightness (default = ?)
	camera.framerate = 32								# set the frame rate 32fps    (max = 60fps)
	rawCapture = PiRGBArray(camera, size=(640, 480))	# 

	# allow the camera to warmup
	time.sleep(0.1)
 
	# capture frames from the camera
	for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
		# grab the raw NumPy array representing the image, then initialize the timestamp
		# and occupied/unoccupied text
		image = frame.array
	 
		# show the frame
		cv2.imshow("Frame", image)
		# Get input key
		key = cv2.waitKey(1) & 0xFF
	 
		# clear the stream in preparation for the next frame
		rawCapture.truncate(0)
	 
		# if the `q` key was pressed, break from the loop
		if key == ord("q"):
			break

if __name__ == "__main__": main()
