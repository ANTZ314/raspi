#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Author:
	Antony Smith
	
Description:
	Single button for both functions (QR code reader & gesture counter)
	Main control class for omnigo IoT project

Includes:
	apds9960 gesture sensor counting method 			- function outside "main"
	PiCamera & OPENCV QR Code reading & storage method	- function outside "main"
	
Notes:
	Threads on each button to run functions behind GUI functionality
	Gesture sensor counter value shown on GUI until stopped
	QR-Code scanner:
		-> exits after 3x confirmed/matched QR reads
		-> else exits after 25 seconds
		-> 'q' exit prematurely

Changes from main:
	Stop Count Click:
		-> store count value to ID's csv-cell
		-> zero GUI counter label
	Error/Info message label
	Remove GUI Exit button
		-> special exit routine??

After changes:
	New ID storage structure
	Old ID recall details
	Black/White List for ID's - menu?
	Transfer csv data (Email/PubSub)

USAGE:
	python main.py
"""
###################
# import packages #
###################
from Tkinter import *					# GUI package
import tkFont							# GUI package
from functools import partial			# passing argument to button?

## MULTI-TASKING FUNCTIONS ##
import threading						# Multi-Threading

## GENERAL MAINTENANCE ##
import sys, time						# Possibly remove ? ?
#from time import sleep					# Delays
import time
import traceback						# Error logging

## 	QR CODE IMPORTS ##
from picamera import PiCamera			# Testing the Camera
from imutils.video import VideoStream	# Video access library
from pyzbar import pyzbar				# Decoding the QR Code
import datetime							# wekking?
import imutils 							# Magic
import cv2								# the eyes of the matrix

## GESTURE IMPORTS ##
from apds9960.const import *
from apds9960 import APDS9960
import smbus

###################
##  GLOBAL DEFS  ##
###################
btn_state1 = 0							# changed to tri-state (0/1/2)
#btn_state2 = True						# removed - only 1 button
csv_file = "barcodes.csv"				# guess what this is?

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
	info = "feedback..."							# GUI feedback information - OPTIONAL
	ID_match = 0									# initial staff ID status

	try:
		try:
			################
			## QR SCANNER ##
			################
			def QR_Scan():
				init_time = time.time()						# no. of secs since 1 Jan 1970
				winName = "SCAN ID"							# name the video window
				scnCnt = 0									# Number of ID confirmations
				done = "n"									# Complete scanning flag
				
				## initialize video stream & warm up camera sensor
				print("[INFO] starting video stream...")
				vs = VideoStream(usePiCamera=True).start()
				time.sleep(2.0)									# Allow video to stabalise
				cv2.namedWindow(winName)
				cv2.moveWindow(winName, 20,20)
				
				## open the output CSV file for writing
				csv = open(csv_file, "w")
				found = set()
				time.sleep(2.0)									# TEST - REMOVE??
				print("[INFO] csv file opened...")
				
				## Loop over the frames from the video stream #
				## Time-Out after 25 secs ##
				while time.time()-init_time < 25:
					## grab the frame from the threaded video stream and r
					## esize it to have a maximum width of 400 pixels
					frame = vs.read()
					frame = imutils.resize(frame, width=400)
				 
					## find & decode the barcodes in each frame
					barcodes = pyzbar.decode(frame)

					## loop over the detected barcodes
					for barcode in barcodes:
						## extract bounding box location & draw around barcode
						(x, y, w, h) = barcode.rect
						cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
				 
						## the barcode data is a bytes object so if we want to draw it
						## on our output image we need to convert it to a string first
						barcodeData = barcode.data.decode("utf-8")
						barcodeType = barcode.type
				 
						## draw the barcode data and barcode type on the image
						text = "{}".format(barcodeData)
						cv2.putText(frame, text, (x, y - 10),
							cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
				 
						## if barcode is not stored, update new one to CSV file
						if barcodeData not in found:
							csv.write("{},{}\n".format(datetime.datetime.now(), barcodeData))
							csv.flush()
							found.add(barcodeData)
							print("[INFO] ID not found.")
						else:
							print("[INFO] ID: {}".format(barcodeData))
							#print("Scan no: {}\n".format(scnCnt))
							scnCnt += 1
						
						## If ID is confirmed 3 times?
						if scnCnt == 3:
							scnCnt = 0					# clear the counter
							done = "y"					# exit the loop

					## FOR FULL SCREEN ? ? ##
					#cv2.namedWindow(winName, cv2.WINDOW_NORMAL)	# create a named window
					#cv2.namedWindow(winName)
					#cv2.moveWindow(winName, 20,20)					# set window placement
					## Get window to full screen ##
					#cv2.setWindowProperty(winName, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN) 
					
					## Show the output frame
					cv2.imshow(winName, frame)
					#cv2.imshow("SCAN ID", frame)
					
					key = cv2.waitKey(1) & 0xFF
				 
					## if the `q` key was pressed, break from the loop
					if key == ord("q"):
						break
					## if ID confirmed 3 times
					elif done == "y":
						break
				
				## close the output CSV file do a bit of cleanup
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
						time.sleep(0.5)
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
			
			##############################
			## BUTTON: EMPLOYEE ID SCAN ##
			##############################
			def btn_start():
				## Gesture counter #
				global GestDone						# Exit Gesture mode flag
				global thr1							# thread flag
				global Cnt							# make global again?
				## ID Scanner #
				global thr2
				global btn_state1					# changed top tri-state
				global info
				
				## Start new thread each time - Counter ##
				if thr1 == 0:
					t1 = threading.Thread(target=get_gesture)	# Not started yet
					threads.append(t1)							# for multiple threads
				
				## Start new thread each time - ID Scan ##
				if thr2 == 0:
					t2 = threading.Thread(target=QR_Scan)	# Not started yet
					threads.append(t2)						# for multiple threads
				
				## START ID SCAN ROUTINE #
				if btn_state1 == 0:
					print("READING QR CODE...")				# REMOVE	
					bigButton["text"] = "START\nCOUNT"
					info = "Info: Video Window Starting..."				
					
					## Update GUI information ##
					update_label()
						
					## If thread not started (can't start twice?)
					if thr2 == 0:
						thr2 = 1							# toggle flag
						t2.start()							# start gesture thread
										
					btn_state1 = 1				# Toggle button flag
					
				## START COUNT ROUTINE #
				elif btn_state1 == 1:
					print("START COUNTING ROUTINE NOW...")	# REMOVE
					bigButton["text"] = "STOP\nCOUNT"		# button label change
					info = "Info: Started Counting..."
					
					## If thread not started (can't start twice?)
					if thr1 == 0:
						thr1 = 1							# toggle flag
						t1.start()							# start gesture thread
					
					## Update GUI information ##
					update_label()
					
					btn_state1 = 2					# Click to end the count
				
				## END COUNT ROUTINE #
				elif btn_state1 == 2:
					print("STOP COUNT")				# temporary - REMOVE
					bigButton["text"] = "START\nCOUNT"
					info = "Info: Counting Complete"
					
					## If thread was started ##
					if thr1 == 1:					# Can't start thread again? - REMOVE?
						thr1 = 0					# Clear thread flag
						GestDone = True				# Break out of Gesture funtion
						## Close the thread ##
						#t1.join()					# ERROR - reference
						
						## Update GUI information ##
						update_label()
					
					btn_state1 = 1					# back to start count?
			
			###########################
			## REALTIME LABEL UPDATE ##
			###########################
			def update_label():
				global Cnt
				global info
				
				# Change label
				label_4.config(text="- {} -".format(Cnt), font = myFont1)
				label_6.config(text="{}".format(info), font = "Helvetica 10")
			
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
			myFont1 = tkFont.Font(family = 'Helvetica', size = 30, weight = 'bold')
			myFont2 = tkFont.Font(family = 'Helvetica', size = 12, weight = 'bold')

			# SETUP WINDOW PARAMTERS ##
			win.title("OMNIGO")						# define window title
			win.geometry('480x320+0+0')				# define screen size
			#win.attributes("-fullscreen", True)	# full screen GUI
			win.configure(background = "gray15")	# set colour
			
			# EXIT BUTTON ##
			exitButton  = Button(win, 
								text 	= "X", 
								font 	= myFont2, 
								command = exitProgram,
								bg		= "gray15",
								fg 		= "gray64",
								height 	= 1 , 
								width 	= 1) 
			exitButton.pack(side=TOP, anchor=NE)
			
			# OMNIGO TITLE ##
			label_2 = Label(win, 
							text 	= "- OMNIGO -", 
							bg 		= "gray15",
							fg 		= "OrangeRed2",
							relief 	= "solid",
							font 	= "Helvetica 36",
							width 	= 11,
							height	= 1)
			# SPACER ##
			label_3 = Label(win, 
							text	= " ", 
							bg 		= "gray15",
							font 	= "Helvetica 18")
			
			# Place objects ##
			#label_1.pack(padx=10)
			label_2.pack(padx=10)
			label_3.pack(padx=10)
			
			# STOP/START BUTTON ##
			bigButton = Button(win, 
								text 	= "SCAN\n- ID -", 
								font 	= myFont1, 
								command = btn_start,	# btn_cnt,
								fg 		= "Red4",
								bg 		= "gray45",
								height 	= 2, 
								width 	= 12)
			bigButton.pack(anchor=CENTER)			# place the object
				
			# SPACER ##
			label_5 = Label(win, 
							text	= " ", 
							bg 		= "gray15",
							font 	= "Helvetica 14")
			# COUNTER ##
			label_4 = Label(win, 
							text	= "- {} -".format(Cnt), 
							fg 		= "OrangeRed2",
							bg 		= "gray15",
							font 	= "Helvetica 30")
			# INFORMATION ##
			label_6 = Label(win, 
							text	= "info: {}".format(info), 
							fg 		= "OrangeRed2",
							bg 		= "gray15",
							font 	= "Helvetica 10")
							
			# Place more objects ##
			label_5.pack(padx=10)					# spcer from button
			label_4.pack(padx=10)					# PCB counter
			label_6.pack(anchor=SW)	# PCB counter
			
			# ##
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
