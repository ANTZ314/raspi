# -*- coding: utf-8 -*-
"""
Description:
Uses picamera to record video of contrast fadde from darkest to lightest

To playback, convert to mp4 first:
MP4Box-fps 30 -add myvid.h264 myvid.mp4
omxplayer myvid.mp4

Run the program like this:
$ python PyPiCam.py
"""
import picamera
from time import sleep

camera = picamera.PiCamera()
camera.resolution = (800,600)		# 60 fps?
camera.rotation = 270				# black mounted camera

# To adjust setting over time
camera.start_preview()

# Video recording for 5 sec
camera.start_recording('PyPiCam3.h264')

for i in range(95):
	camera.brightness = i
	sleep(0.3)

camera.stop_recording()
# Stop preview
camera.stop_preview()
