## OpenCV3 with Python 2? ##
import cv2
import sys

class faceCntClass:
	# Define image file names
	file0 = '/home/antz/0_CV3/pics/gr0.jpg'
	
	def __init__(self, **kwargs):
		print("Powering up!!")
		
	def message(self, string):
		print("Checking for {0}\n".format(str(string)))
		
	def FaceCounter(self):
		# Get user supplied values
		imagePath = self.file0								#sys.argv[1]
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
		#print ("Found {0} faces!".format(FaceNum))

		# Draw a rectangle around the faces
		for (x, y, w, h) in faces:
			cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
		
		cv2.imshow("Faces found", image)					# Show the image with faces outlined
		cv2.waitKey(0)										# Wait for key press to exit
		
		return FaceNum
		
	def UseFace(self, FaceNum):
		print("Found {0} faces!".format(FaceNum))
		exists = 0											# Append after printing contents
		try:												# Skip if file doesn't exist
			file = open('FaceCount.txt', 'r') 				# Open to read file
			print (file.read())								# Print the contents
			file.close()									# Close the file
		except:
			exists = 1										# Don't append twice if file exists
			file= open("FaceCount.txt","a+")				# Create/open file then Append data 
			file.write("Image Path: {0}\r\n".format(self.file0))
			file.write("Number of faces: {0}\r\n".format(FaceNum))
			file.close()									# Exit the opened file

		if exists == 0:										# Append after printing contents
			file= open("FaceCount.txt","a+")				# Create/open file then Append data 
			file.write("Image Path: {0}\r\n".format(self.file0))
			file.write("Number of faces: {0}\r\n".format(FaceNum))
			file.close()									# Exit the opened file
		else:												# Notify of file creation
			print ("\nThe File was created...")				# notification	
