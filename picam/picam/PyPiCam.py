# -*- coding: utf-8 -*-
"""
Description:
Uses picamera to capture image

Run the program like this:
$ python PyPiCam.py
"""
import picamera
import time, sys

# create an instance
camera = picamera.PiCamera()

# To flip views
camera.hflip = True
camera.vflip = True

#crop camera
camera.crop = (0.0, 0.0, 1.0, 1.0)

#view overlay
camera.start_preview()
# delay 1 sec
time.sleep(1)
# Stop overlay
camera.stop_preview()

# Take a picture
camera.capture('image0.jpg')

sys.exit(0)
