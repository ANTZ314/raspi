# -*- coding: utf-8 -*-
"""
capture test
"""

from time import sleep
from picamera import PiCamera
import sys	
	
def main():
	camera = PiCamera()
	PiCamera.CAPTURE_TIMEOUT = 10		# IF FREEZES THEN EXITS AFTER 10 SEC?
	camera.resolution = (1024,768)
	camera.start_preview()
	sleep(2)
	camera.capture('foo.jpg', use_video_port=True)
	sys.exit()

		
if __name__ == "__main__":	main()
