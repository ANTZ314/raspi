import cv2
import sys

#-- Get user supplied values --#
#imagePath = sys.argv[1]		# loads the image (first argument in file path)
#cascPath = sys.argv[2]			# loads the path to the cascade file (in directory)

#-- Create the haar cascade --#
#faceCascade = cv2.CascadeClassifier(cascPath)
faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
imagePath = 'jpop1.jpg'

#-- Read the image --#
image = cv2.imread(imagePath)					# load the image path
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)	# Convert to greyscale
# -> Fails loading image if already in Greyscale

#-- Detect faces in the image --#
faces = faceCascade.detectMultiScale(
    gray,
    scaleFactor=1.1,
    minNeighbors=5,
    minSize=(30, 30),
    flags = cv2.cv.CV_HAAR_SCALE_IMAGE
)

print "Found {0} faces!".format(len(faces))

#-- Draw a rectangle around the faces --#
for (x, y, w, h) in faces:
    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

cv2.imshow("Faces found", image)
cv2.waitKey(0)
