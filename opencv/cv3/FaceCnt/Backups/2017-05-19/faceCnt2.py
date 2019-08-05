## OpenCV3 with Python 2? ##
import cv2
import sys
import os

class faceCntClass:
	# Define image file path:
	#file0 = '../pics'										
	file0 = '/home/antz/0_CV3/pics'
	file1 = '/home/antz/0_CV3/pics/gr0.jpg'				# single image
	
	def __init__(self, **kwargs):
		print("Powering up!!")
		
	def message(self, string):
		print("Checking for {0}\n".format(str(string)))
	
	def fcount(self, path):
		""" Counts the number of files in a directory """
		count = 0
		for f in os.listdir(path):
			if os.path.isfile(os.path.join(path, f)):
				count += 1
		return count
	
	def No_images(self):
		Image_No = 0
		Image_No = self.fcount(self.file0)						# get the number of files
		print("Found {0} files!\n".format(Image_No))			# display the number of images at that path
		return Image_No
		
	def FaceCounter(self):
		# Get user supplied values
		imagePath = self.file1								#sys.argv[1]
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
		
	def UseFace(self, FaceNum, count):
		print("Found {0} faces!".format(FaceNum))
		exists = 0											# Append after printing contents
		try:												# Skip if file doesn't exist
			file = open('FaceCount.txt', 'r') 				# Open to read file
			print ("File Contents:")
			print("=" * 20)
			print(file.read())								# Print the contents			
			file.close()									# Close the file
		except:
			exists = 1										# Don't append twice if file exists
			file= open("FaceCount.txt","a+")				# Create/open file then Append data 
			#file.write("=" * 20)							# creat border
			#file.write("Image Path: {0}\r\n".format(self.file0))
			file.write("\nFilename: {0}\r\n".format(os.listdir(self.file0)[count]))
			file.write("Number of faces: {0}\r\n".format(FaceNum))
			file.close()									# Exit the opened file

		if exists == 0:										# Append after printing contents
			file= open("FaceCount.txt","a+")				# Create/open file then Append data 
			#file.write("Image Path: {0}\r\n".format(self.file0))
			file.write("Filename: {0}\r\n".format(os.listdir(self.file0)[count]))
			file.write("Number of faces: {0}\r\n".format(FaceNum))
			file.close()									# Exit the opened file
			print ("{0} was appended".format(os.listdir(self.file0)[count])) # notification
		else:												# Notify of file creation
			print ("\nThe File was created...")				# notification	
