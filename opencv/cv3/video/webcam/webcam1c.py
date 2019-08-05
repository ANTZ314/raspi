# -*- coding: utf-8 -*-
"""
Description:
Opens default webcam, increases brightness for indoor use and detects faces
Press and hod "q" to exit

Run the program like this:
$ python webcam.py
"""
# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import sys

# Get classifier
cascPath = "haarcascade_frontalface_default.xml"	# sys.argv[1]
faceCascade = cv2.CascadeClassifier(cascPath)

def main():
	# initialize the camera and grab a reference to the raw camera capture
	camera = PiCamera()
	camera.resolution = (640, 480)						# set the image resolution	  (max = ?)
	camera.brightness = 65								# increase default brightness (default = ?)
	camera.framerate = 32								# set the frame rate 32fps    (max = 60fps)
	rawCapture = PiRGBArray(camera, size=(640, 480))	# 

	# allow the camera to warmup
	time.sleep(0.1)
	
	# capture frames from the camera
	for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
		# grab the raw NumPy array representing the image, then initialize the timestamp
		# and occupied/unoccupied text
		image = frame.array
		
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		faces = faceCascade.detectMultiScale(gray, 1.3, 5)
		
		# Draw a rectangle around the faces
		for (x, y, w, h) in faces:
			cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
		
		# show the video
		cv2.imshow('Video', image)
		
		# Get input key
		key = cv2.waitKey(1) & 0xFF
		
		# clear the stream in preparation for the next frame
		rawCapture.truncate(0)
		
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
	
	# When everything is done, release the capture
	cv2.destroyAllWindows()
	print("Destroy & Exit!!")

if __name__ == "__main__": main()
