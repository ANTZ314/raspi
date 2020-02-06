# -*- coding: utf-8 -*-
"""
Description:
Continuous camera display

Command line camera test:
vcgencmd get_camera 	-> supported = 1, detected = 1
raspistill -o pic.jpg

Use:
python cam_test.py
"""
from picamera import PiCamera
from time import sleep

camera = PiCamera()

camera.start_preview()
sleep(5)
camera.stop_preview()