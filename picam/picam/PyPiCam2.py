# -*- coding: utf-8 -*-
"""
Description:
Uses picamera to capture 2 images then
fades from darkest contrast to lightest
& should record 5 seconds of video

Run the program like this:
$ python PyPiCam.py
"""
import picamera
from time import sleep

camera = picamera.PiCamera()
#camera.resolution(640,480)		# video resolution
camera.rotation = 270			# black mounted camera

# Using a pause btwn shots
camera.capture('image1.jpg')
sleep(5)
camera.capture('image2.jpg')

# To adjust setting over time
camera.start_preview()
# Video recording for 5 sec
camera.start_recording('PyPiCam2.h264')
sleep(5)
# Guess what this does?
camera.stop_recording()
