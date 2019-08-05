# -*- coding: utf-8 -*-
"""
Make sure installed:
pip install "picamera[array]

Description: 
Opens the specified video file and displays in new window
"q" to quit

Run:
$ python pivid1.py test2.mp4
"""
import cv2
import sys

# Get classifier
cascPath = "haarcascade_frontalface_default.xml"	# sys.argv[1]
faceCascade = cv2.CascadeClassifier(cascPath)

# Open the video file
filename = sys.argv[1]
video_capture = cv2.VideoCapture(filename)			# use video file name?
#video_capture = cv2.VideoCapture(0)					# get default camera module

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
