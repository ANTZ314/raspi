# -*- coding: utf-8 -*-
## OpenCV3 with Python 2.x ##
# To Run:
# python face_detect.py /image/path/image.jpg
import cv2
import sys

# Get user supplied values
imagePath = sys.argv[1]		# Path: ../pics/gr1.jpg
#cascPath = sys.argv[2]

# Create the haar cascade
#faceCascade = cv2.CascadeClassifier(cascPath)
faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Read the image
image = cv2.imread(imagePath)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Detect faces in the image
faces = faceCascade.detectMultiScale(
    gray,
    scaleFactor=1.15,
    minNeighbors=5,
    minSize=(30, 30)
    #flags = cv2.CV_HAAR_SCALE_IMAGE
)

print ("Found {0} faces!".format(len(faces)))

# Draw a rectangle around the faces
for (x, y, w, h) in faces:
    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

cv2.imshow("Faces found", image)
cv2.waitKey(0)
