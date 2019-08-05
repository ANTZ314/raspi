# -*- coding: utf-8 -*-
"""
Playback video file:
http://docs.opencv.org/3.1.0/dd/d43/tutorial_py_video_display.html
Description:
Simple example of using cv2 to playback video source frame-by-frame with
'waitkey(x)' value determining the playback frame-rate
All other settings are default
"""
import numpy as np
import cv2
cap = cv2.VideoCapture('sample.mpg')
 
while(cap.isOpened()):
	# Capture frame-by-frame
	ret, frame = cap.read()
	
	# Our operations on the frame come here
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	
	# Display the resulting frame
	cv2.imshow('frame',gray)
	
	# 'q' to quit [wait value determines playback speed]
	if cv2.waitKey(25) & 0xFF == ord('q'):		# 25fps?
		break
		
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
