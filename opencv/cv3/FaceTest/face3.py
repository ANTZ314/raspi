import cv2
import sys

#-- Get user supplied values --#
imagePath = 'gr0.jpg'
faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

#-- Read the image --#
image = cv2.imread(imagePath)					# load the image path
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)	# Convert to greyscale

#-- Detect faces in the image --#
faces = faceCascade.detectMultiScale(
    gray,
    scaleFactor=1.075,		# Determines face count accuracy [1.0 - 1.2]
    minNeighbors=5,
    minSize=(30, 30),
)

#-- Print the number of faces found --#
print ("Found {0} faces!".format(len(faces)))

#-- Draw a rectangle around the faces --#
for (x, y, w, h) in faces:
    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

cv2.imshow("Faces found", image)
cv2.waitKey(0)
