"""
DESCRIPTION:
Real-time barcode and QR code reading with OpenCV

DEPENDENCIES:
OpenCV
sudo apt-get install libzbar0
sudo pip install pyzbar
sudo pip install imutils

USE:
python scanner2.py
'q' to quit
"""
# import the necessary packages
from imutils.video import VideoStream
from pyzbar import pyzbar
import argparse
import datetime
import imutils
import sys, time
import cv2

try:
	scnCnt = 0			# count number of ID confirmations
	done = "n"			# complete scanning flag
	
	# construct the argument parser and parse the arguments
	ap = argparse.ArgumentParser()
	ap.add_argument("-o", "--output", type=str, default="barcodes.csv",
		help="path to output CSV file containing barcodes")
	args = vars(ap.parse_args())

	# initialize the video stream and allow the camera sensor to warm up
	print("[INFO] starting video stream...")
	# vs = VideoStream(src=0).start()
	vs = VideoStream(usePiCamera=True).start()
	time.sleep(2.0)

	# open the output CSV file for writing and initialize the set of
	# barcodes found thus far
	csv = open(args["output"], "w")
	found = set()

	# loop over the frames from the video stream
	while True:
		# grab the frame from the threaded video stream and resize it to
		# have a maximum width of 400 pixels
		frame = vs.read()
		frame = imutils.resize(frame, width=400)
	 
		# find the barcodes in the frame and decode each of the barcodes
		barcodes = pyzbar.decode(frame)

		# loop over the detected barcodes
		for barcode in barcodes:
			# extract bounding box location & draw around barcode
			(x, y, w, h) = barcode.rect
			cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
	 
			# the barcode data is a bytes object so if we want to draw it
			# on our output image we need to convert it to a string first
			barcodeData = barcode.data.decode("utf-8")
			barcodeType = barcode.type
	 
			# draw the barcode data and barcode type on the image
			text = "{}".format(barcodeData)
			cv2.putText(frame, text, (x, y - 10),
				cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
	 
			# if barcode is not stored, update new one to CSV file
			if barcodeData not in found:
				csv.write("{},{}\n".format(datetime.datetime.now(), barcodeData))
				csv.flush()
				found.add(barcodeData)
				print("ID not found.")
			else:
				print("ID: {}".format(barcodeData))
				#print("Scan no: {}\n".format(scnCnt))
				scnCnt += 1
			
			# If ID is confirmed 3 times?
			if scnCnt == 3:
				scnCnt = 0		# clear the counter
				done = "y"		# exit the loop

		# show the output frame
		cv2.imshow("Barcode Scanner", frame)
		key = cv2.waitKey(1) & 0xFF
	 
		# if the `q` key was pressed, break from the loop
		if key == ord("q"):
			break
		elif done == "y":
			break
	 
	# close the output CSV file do a bit of cleanup
	print("[INFO] cleaning up...")
	csv.close()
	cv2.destroyAllWindows()
	vs.stop()
	sys.exit(0)

# Any Main Errors saved to log.txt file:
except Exception:
	print("main.py - Exception reached")
	log = open("log.txt", 'w')
	traceback.print_exc(file=log)
	sys.exit(0)
