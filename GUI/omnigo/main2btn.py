#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Author:
	Antony Smith
	
Description:
	2 Button version
	Main control class for omnigo IoT project

Includes:
	apds9960 gesture sensor counting method 			- function outside "main"
	PiCamera & OPENCV QR Code reading & storage method	- function outside "main"
	
Notes:
	This version has working threads from each button
	Gesture sensor counter is shown on GUI until stopped
	OpenCV not destroying window properly

USAGE:
	python main.py
"""
###################
# import packages #
###################
from Tkinter import *					# GUI package
import tkFont							# GUI package
from functools import partial			# passing argument to button?

import threading						# Multi-Threading

import sys, time						# Possibly remove ? ?
from time import sleep					# Delays
import traceback						# Error logging

## 	QR CODE IMPORTS ##
from picamera import PiCamera			# Testing the Camera
from imutils.video import VideoStream	# Video access library
from pyzbar import pyzbar				# Decoding the QR Code
import datetime							# piece of shit
import imutils 							# Magic
import cv2

## GESTURE IMPORTS ##
from apds9960.const import *
from apds9960 import APDS9960
import smbus

###################
##  GLOBAL DEFS  ##
###################
btn_state1 = True
btn_state2 = True
csv_file = "barcodes.csv"

port = 1
bus  = smbus.SMBus(port)
apds = APDS9960(bus)


###################
## MAIN FUNCTION ##
###################
def main():
	global thr1										# thread flag
	global thr2										# thread flag
	global Cnt										# PCB count value
	global GestDone									# Exit Gesture mode flag
	
	GestDone = False								# initial state
	Cnt = 0											# Counter start value
	
	ID_match = 0									# initial staff ID status
	
	try:
		try:
			################
			## QR SCANNER ##
			################
			def QR_Scan():
				winName = "SCAN ID"
				scnCnt = 0			# count number of ID confirmations
				done = "n"			# complete scanning flag
				
				# initialize the video stream and allow the camera sensor to warm up
				print("[INFO] starting video stream...")
				vs = VideoStream(usePiCamera=True).start()
				sleep(2.0)									# Allow video to stabalise
				cv2.namedWindow(winName)
				cv2.moveWindow(winName, 20,20)
				
				# open the output CSV file for writing
				csv = open(csv_file, "w")
				found = set()
				sleep(2.0)									# TEST - REMOVE??
				
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
							scnCnt = 0					# clear the counter
							done = "y"					# exit the loop

					
					#cv2.namedWindow(winName, cv2.WINDOW_NORMAL)	# create a named window
					#cv2.namedWindow(winName)
					#cv2.moveWindow(winName, 20,20)					# set window placement
					## Get window to full screen
					#cv2.setWindowProperty(winName, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN) 
					
					## Show the output frame
					cv2.imshow(winName, frame)
					#cv2.imshow("SCAN ID", frame)
					
					key = cv2.waitKey(1) & 0xFF
				 
					# if the `q` key was pressed, break from the loop
					if key == ord("q"):
						break
					# if ID confirmed 3 times
					elif done == "y":
						break
				
				# close the output CSV file do a bit of cleanup
				print("[INFO] cleaning up...")
				csv.close()								# close excel document
				vs.stop()								# stop video stream
				cv2.destroyAllWindows()					# not destroying??
				#cv2.destroyWindow("Stall ID")			# destroy specific window
				lift_window()							# Put GUI on the top
	
			#####################
			## GESTURE COUNTER ##
			#####################
			def get_gesture():
				global Cnt					# Double defined?
				Cnt = 0						# Double defined?
				global GestDone				# Exit Gesture flag
				GestDone = False			# Exit Gesture flag
				exitCnt = 0					# Exit count mode flag
				direct = 'none'				# Direction of swipe
				
				dirs = {
					APDS9960_DIR_NONE:  "none",
					APDS9960_DIR_LEFT:  "left",
					APDS9960_DIR_RIGHT: "right",
					APDS9960_DIR_UP:    "up",
					APDS9960_DIR_DOWN:  "down",
					APDS9960_DIR_NEAR:  "near",
					APDS9960_DIR_FAR:   "far",
					}
				try:
					# Set the proximity threshold
					apds.setProximityIntLowThreshold(50)
						
					print("CAPTURE GESTURES:")
					print("=================")
					apds.enableGestureSensor()
					while True:
						sleep(0.5)
						if apds.isGestureAvailable():
							motion = apds.readGesture()
							direct = dirs.get(motion, "unknown")
							#print("Gesture = {}".format(direct))
							if direct == "left":
								Cnt += 1				# May need upper limit?
							elif direct == "up":
								Cnt += 1				# May need upper limit?
							elif direct == "right":
								if Cnt > 0:				# Avoid negative situations
									Cnt -= 1
							elif direct == "down":
								if Cnt > 0:				# Avoid negative situations
									Cnt -= 1
							
							## Continuously update GUI Label ##
							update_label()
							print("PCB Count: {}".format(Cnt))
							
						####################################	
						# Increment exit counter	- REMOVE 
							exitCnt += 1				
						# After 'x' swipes 			- REMOVE 
						if exitCnt == 7:
							GestDone = True
						####################################	
						
						## Break from loop early ##
						if GestDone == True:
							break
				
				## Do before exiting Gesture Mode ##		
				## Unecessary - REMOVE ##
				finally:
					print ("Final Board Count: {}".format(Cnt))
			
			## Intialise both Threads (not started yet) ##
			threads = []							# create thread list
			thr1 = 0								# thread 1 flag
			thr2 = 0								# thread 2 flag
			
			#t1 = threading.Thread(target=get_gesture)
			#t2 = threading.Thread(target=QR_Scan)	
			
			##############################
			## BUTTON: EMPLOYEE ID SCAN ##
			##############################
			def btn_scan():
				global thr2
				global btn_state1
				
				## Start new thread each time ##
				if thr2 == 0:
					t1 = threading.Thread(target=QR_Scan)	# Not started yet
					threads.append(t1)						# for multiple threads
				
				## First click of the Cam Button ##
				## CHANGE TO ONLY CLICK OF CAM BUTTON ? ? ##
				if btn_state1 == False:
					print("READING QR CODE...")		# REMOVE
					scanButton["text"] = "STOP\nSCAN"
					## If thread not started (can't start twice?)
					if thr2 == 0:
						thr2 = 1					# toggle flag
						t2.start()					# start gesture thread
										
					btn_state1 = not btn_state1		# Toggle button flag
				## DOES NOTHING HERE - REMOVE
				else:
					scanButton["text"] = "SCAN\n-ID-"
					## Destroy the window here again??
					#cv2.destroyAllWindows()		# does nothing??
					#lift_window()					# Bring main GUI to top
					print("Do nothing - REMOVE")	
					btn_state1 = not btn_state1		# Toggle button flag
			
			#############################
			## BUTTON: GESTURE COUNING ##
			#############################
			def btn_cnt():
				global GestDone						# Exit Gesture mode flag
				global thr1							# thread flag
				global btn_state2					# toggling button state
				global Cnt							# make global again?
				
				## Start new thread each time ##
				if thr1 == 0:
					t1 = threading.Thread(target=get_gesture)	# Not started yet
					threads.append(t1)							# for multiple threads
				
				## Click1 ##
				if btn_state2 == False:
					print("START COUNT")			# temporary - REMOVE
					cntButton["text"] = "STOP\nCOUNT"
					## If thread not started (can't start twice?)
					if thr1 == 0:
						thr1 = 1					# toggle flag
						t1.start()					# start gesture thread
					
					## Update initial count value ##
					## -> REDUNDANT: Unless continuing count
					update_label()
					
					btn_state2 = not btn_state2		# toggle button flag
				
				## Click2 ##
				else:
					print("STOP COUNT")				# temporary - REMOVE
					cntButton["text"] = "START\nCOUNT"
					## If thread was started ##
					if thr1 == 1:					# Can't start thread again? - REMOVE?
						thr1 = 0					# Clear thread flag
						GestDone = True				# Break out of Gesture funtion
						## Close the thread ##
						#t1.join()					# ERROR - reference
						
						## Show the final count on the GUI
						update_label()
					
					btn_state2 = not btn_state2		# toggle button flag
			
			###########################
			## REALTIME LABEL UPDATE ##
			###########################
			def update_label():
				global Cnt
				# Change label
				label_4.config(text="Count: {}".format(Cnt), font = myFont2)
			
			#########################
			## BRING WINDOW TO TOP ##
			#########################
			def lift_window():
				print("Lift Window")
				win.lift()
			
			##########################
			## EXIT AND DESTROY GUI ##
			##########################
			def exitProgram():
				global thr1
				
				if thr1 == 0:
					print("Exit Button Pressed")
					win.quit()
				else:
					print("Still busy...")	


			## INITIALISE NEW WINDOW ##
			win = Tk()
			## Define the Fonts:
			myFont1 = tkFont.Font(family = 'Helvetica', size = 24, weight = 'bold')
			myFont2 = tkFont.Font(family = 'Helvetica', size = 12, weight = 'bold')

			# SETUP WINDOW PARAMTERS ##
			win.title("OMNIGO")						# define window title
			win.geometry('480x320+0+0')				# define screen size
			#win.attributes("-fullscreen", True)	# full screen GUI
			win.configure(background = "darkblue")	# set colour
			
			# SPACER ##
			label_1 = Label(win, 
							text	= " ",
							bg 		= "darkblue",
							font 	= "Helvetica 10")
			# OMNIGO TITLE ##
			label_2 = Label(win, 
							text 	= "- OMNIGO -", 
							bg 		= "darkblue",
							fg 		= "white",
							relief 	= "solid",
							font 	= "Times 24",
							width 	= 11,
							height	= 1)
			# SPACER ##
			label_3 = Label(win, 
							text	= " ", 
							bg 		= "darkblue",
							font 	= "Helvetica 10")
			# PCB COUNT ##
			label_4 = Label(win, 
							text	= "Count: {}".format(Cnt), 
							fg 		= "white",
							bg 		= "darkblue",
							font 	= "Helvetica 14")
			
			label_1.pack()
			label_2.pack()
			label_3.pack()
			label_4.pack()

			# EXIT BUTTON ##
			exitButton  = Button(win, 
								text 	= "Exit", 
								font 	= myFont1, 
								command = exitProgram, 
								height 	= 1 , 
								width 	= 5) 
			exitButton.pack(side = BOTTOM)

			# ID SCAN BUTTON ##
			scanButton = Button(win, 
								text 	= "SCAN", 
								font 	= myFont1, 
								command = btn_scan,
								fg 		= "darkgreen",
								bg 		= "white",
								height 	= 3, 
								width 	= 10)
			scanButton.pack(side = LEFT)
			
			# COUNT BUTTON ##
			cntButton = Button(win, 
								text 	= "COUNT", 
								font 	= myFont1, 
								command = btn_cnt,
								fg 		= "darkgreen",
								bg 		= "white",
								height 	= 3, 
								width 	= 10)
			cntButton.pack(side = RIGHT)

			mainloop()
			
		# Ctrl+C will exit the program correctly
		except KeyboardInterrupt:
			print("main.py - keyboard interupt")
			sys.exit(0)
		
	# Any Main Errors saved to log.txt file:
	except Exception:
		print("main.py - Exception reached")
		log = open("log.txt", 'w')
		traceback.print_exc(file=log)
		sys.exit(0)


if __name__ == "__main__":	main()
