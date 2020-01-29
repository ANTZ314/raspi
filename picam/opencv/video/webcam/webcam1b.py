# -*- coding: utf-8 -*-
"""
Description:
Opens default webcam and detects faces - not opening camera?

Run the program like this:
$ python webcam.py
"""
import cv2
import sys

# Get classifier
cascPath = "haarcascade_frontalface_default.xml"	# sys.argv[1]
faceCascade = cv2.CascadeClassifier(cascPath)

# Capture from Camera
cap = cv2.VideoCapture(0)				# doesn work	?
#cap = cv2.VideoCapture("test2.mp4")	# works			?

def main():
	while cap.isOpened():
		# Capture frame-by-frame
		ret, frame = cap.read()#FFFFFF
		if ret:
			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			faces = faceCascade.detectMultiScale(gray, 1.3, 5)
			
			# Draw a rectangle around the faces
			for (x, y, w, h) in faces:
				cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

			# Display the resulting frame
			cv2.imshow('Video', frame)

			if cv2.waitKey(1) & 0xFF == ord('q'):
				break

	# When everything is done, release the capture
	cap.release()
	cv2.destroyAllWindows()
	print("Destroy & Exit!!")

if __name__ == "__main__": main()
