
"""
# -*- coding: utf-8 -*-
""
Created on: 	[2017-05-09]
@author: 		Antony Smith
@description: 	
""
import faceCnt2 as FaceCnt

def main():
    # Instantiate the class
    Face = FaceCnt.faceCntClass()       # Create object to access 'FaceCnt' Class
    Face.message("Images...")			# Pass text message to the class
    
    FaceNum = Face.FaceCounter()        # Call the main Face Finder
    Face.UseFace(FaceNum)  				# Use the number of faces  
    print"Complete..."
    
if __name__ == "__main__": main()
"""

## OpenCV3 with Python 2? ##
import cv2
import sys

# Get user supplied values
imagePath = sys.argv[1]
cascPath = sys.argv[2]

# Create the haar cascade## OpenCV3 with Python 2? ##
import cv2
import sys

class faceCntClass:
	def __init__(self, **kwargs):
		print("Anything!!")
		
	def message(self, string):
		print("Checking {0}\n".format(str(string)))
		
	def FaceCounter(self):
		# Get user supplied values
		imagePath = '/home/antz/0_CV3/pic/gr0.jpg'			#sys.argv[1]
		cascPath = 'haarcascade_frontalface_default.xml'	#sys.argv[2]
		
		# Create the haar cascade
		faceCascade = cv2.CascadeClassifier(cascPath)
		
		# Read the image
		image = cv2.imread(imagePath)
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		
		
		# Detect faces in the image
		faces = faceCascade.detectMultiScale(
			gray,											# 
			scaleFactor=1.1,								# 
			minNeighbors=5,									# 
			minSize=(30, 30)								# 
			#flags = cv2.CV_HAAR_SCALE_IMAGE				# using CV3..?
		)

		# Get the number of face found in the image
		FaceNum = len(faces)
		#print "Found {0} faces!".format(FaceNum)

		# Draw a rectangle around the faces
		for (x, y, w, h) in faces:
			cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
		
		#cv2.imshow("Faces found", image)					# Show the image with faces outlined
		#cv2.waitKey(0)										# Wait for key press to exit
		
		return FaceNum
		
	def UseFace(self, FaceNum):
		print("Found {0} faces!".format(FaceNum))

faceCascade = cv2.CascadeClassifier(cascPath)

# Read the image
image = cv2.imread(imagePath)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Detect faces in the image
faces = faceCascade.detectMultiScale(
    gray,
    scaleFactor=1.1,
    minNeighbors=5,
    minSize=(30, 30)
    #flags = cv2.CV_HAAR_SCALE_IMAGE
)

print "Found {0} faces!".format(len(faces))

# Draw a rectangle around the faces
for (x, y, w, h) in faces:
    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

cv2.imshow("Faces found", image)
cv2.waitKey(0)

