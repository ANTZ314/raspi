# -*- coding: utf-8 -*-
"""
Description:
Receives a number of days and number of frames per hour
Captures images according to these values
OR
Number of seconds between each capture?
"""
import time
import picamera

class captureClass:
	VIDEO_DAYS = 1
	FRAMES_PER_HOUR = 60
	
	def capture_frame(self, frame):
		with picamera.PiCamera() as cam:
			time.sleep(2)
			cam.capture('/home/pi/Pictures/timelapse/frame%03d.jpg' % frame)

	def capture(self, days, frames)
		## Check if both intergers ##
		check1 = days.isdigit()
		check2 = frames.isdigit()
		if check1 == True && check2 == True:
			VIDEO_DAYS = days
			FRAMES_PER_HOUR = frames
		else:
			print("Value entered was not valid!")
		## New value else default value ##
		FRAMES = FRAMES_PER_HOUR * 24 * VIDEO_DAYS
		
		# Capture the images							<------ Will stay in this loop until value reached!
		for frame in range(FRAMES):
			# Note the time before the capture
			start = time.time()
			capture_frame(frame)

			## Wait for the next capture. Note that we take into
			## account the length of time it took to capture the
			## image when calculating the delay
			time.sleep( int(60 * 60 / FRAMES_PER_HOUR) - (time.time() - start) )
