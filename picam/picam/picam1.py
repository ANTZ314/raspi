# -*- coding: utf-8 -*-
"""
Description:
Opens the camera module, captures single frame and displays
Press any key to kill

First use:
pip install "picamera[array]

Run: 
python2 picam1.py
--------------------
"""
# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

def main(): 
	# initialize the camera and grab a reference to the raw camera capture
	camera = PiCamera()
	rawCapture = PiRGBArray(camera)
	 
	# allow the camera to warmup
	time.sleep(0.1)
	 
	# grab an image from the camera
	camera.capture(rawCapture, format="bgr")
	image = rawCapture.array
	 
	# display the image on screen and wait for a keypress
	cv2.imshow("Image", image)
	cv2.waitKey(0)

if __name__ == "__main__": main()
