#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Author:
	Antony Smith - T.S.E. [July 2020]

Description:
	THIS VERSION IS FOR 4 DEMO UNITS - (MAKE FULL SCREEN)
	GCP MQTT to ~MY~ GC-Platform
	Main control GUI for Omnigo IoT project
	Raspberry Pi Zero + PiCamera + APDS9960

Primary Functions:
	GUI functionality:
		-> Widget placement + Colour schemes			- [complete]
		-> Real-time label udpates (count/info)			- [complete]
		-> Multi-Threading								- [complete]
		-> multiple windows in parallel operation		- [complete]
	APDS9960 gesture sensor counting method 			- [complete]
	PiCamera & OPENCV QR Code reading					- [complete]
	Scan Kit & Staff ID + storage method				- [complete]
	Exit code required to leave GUI						- [complete]
	Drop-down menu stage selector						- [complete]
	JSON data format conversion							- [complete]
	Upload data to Google Cloud IoT-Core [MINE]			- [complete]

Changes required:
	cv2 Camera window NOT destroyed						- [incomplete]
	Counter thread NOT ending							- [incomplete]
	Re-Scan ID's later?									- [incomplete]
		
Notes:
	GUI EXIT CODE: 3529# ('*' to Delete)
	QR-Code scanner:
		-> exits after 3x confirmed QR reads
		-> 'q' exit prematurely
	GCP connectivity requires:
		-> 'jwt_maker.py' to create JWT security key
		-> ssl security files: 
			=> roots.pem
			=> rsa_private.pem

USAGE:
	python main.py
"""
###################
# import packages #
###################

## GUI PACKAGES ##
from Tkinter import *					# GUI package
import tkFont							# GUI package
from functools import partial			# passing argument to button?

## MULTI-TASKING FUNCTIONS ##
import threading						# Multi-Threading

## GENERAL MAINTENANCE ##
import sys								# Possibly remove ? ? ?
import time								# time travel
import traceback						# Error logging
import datetime							# Get real-time data

## 	QR CODE IMPORTS ##
from picamera import PiCamera			# Testing the Camera
from imutils.video import VideoStream	# Video access library
from pyzbar import pyzbar				# Decoding the QR Code
import imutils 							# A little slice of Magic
import cv2								# When you stare into the matrix...

## GESTURE IMPORTS ##
from apds9960.const import *
from apds9960 import APDS9960
import smbus

## JSON File and GCP ##
import json								# JSON conversion functions
import jwt								# Create JSON security token 
import paho.mqtt.client as mqtt			# MQTT connectivity


###################
##  GLOBAL DEFS  ##
###################
btn_state1 = 0										# changed to tri-state (0/1/2)
csv_file = "barcodes.csv"							# guess what this is?
OptionList = ["SETUP","THRU","SMT","INSP","EXIT"] 	# Drop Down Menu Options
# Some technical requirements
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
	global pin	 									# Exit Code Value
	global CodeDone									# Exit Code - flag
	global qrData									# Get QR Data
	global iotJSON									# Converted to JSON format
	global firstScan								# (createJSON) - only store certain data on first scan
	global projectStat					# (createJSON) - project start or stop
	global staffID						# (createJSON) - Extracted Staff ID
	
	lay=[]											# layering windows??
	CodeDone = False								# Exit Code - negative
	pin  = ''										# Exit Code - blank string
	GestDone = False								# Gesture count - flag
	Cnt = 0											# PCB Counter start value
	info = "feedback..."							# GUI feedback information - OPTIONAL
	ID_match = 0									# ID Scan - initial staff ID status
	qrData = "data from qr code"					# initialise to string format
	iotJSON = "upload"								# initialise to string format
	firstScan = 0									# initialise for 1st data update
	staffKit = 0									# initialise to kit_ID 1st
	
	## Define some project-based variables to be used below ##
	ssl_private_key_filepath = './certs/rsa_private.pem'  # '<ssl-private-key-filepath>'
	ssl_algorithm            = 'RS256'                    # '<algorithm>' # Either RS256 or ES256
	root_cert_filepath       = './certs/roots.pem'        # '<root-certificate-filepath>'
	project_id               = 'iot-omnigo1'              # '<GCP project id>'
	gcp_location             = 'us-central1'              # '<GCP location>'
	registry_id              = 'omnigo_registry'          # '<IoT Core registry id>'
	device_id                = 'omnigo_device1'           # '<IoT Core device id>'
	
	## Proiject Information dictionary ##
	global dataDict
	dataDict = {'CLIENT'	: 'xxx',			# Client Name
				'PROJECT'	: '0',				# Project ID
				'STAGE'		: 'xxx',			# Operational Stage (setup/smt/thru/insp)
				'BOARDS'	: '0',				# Number PC-Boards
				'PANELS'	: '0',				# Number of panels
				'STAFF_ID'	: '0',				# Staff member ID number
				'DATE'		: '00-00-2020',		# Project start date
				'TIME'		: '00:00',			# Time of each board swiped
				'START'		: '00:00',			# Stage - start time 
				'STOP'		: '00:00',			# Stage - end time
				'REASON'	: 'null',			# Reason the stage was stopped
				'SERIAL'	: '0' }				# Barcode serial number - Later

	## Get the current time/date ##
	cur_time = datetime.datetime.utcnow()
	
	try:
		try:
			################
			## QR SCANNER ##
			################
			def QR_Scan():
				global qrData									# globalise QR Data
				global staffID									# Extracted Staff ID
				init_time = time.time()							# no. of secs since 1 Jan 1970
				winName = "SCAN-ID"								# name the video window
				scnCnt = 0										# Number of ID confirmations
				done = "kit"									# which scan is complete
				staffKit = 0									# Which ID - kit_ID[0] / Staff_ID[1]
				
				
				## initialize video stream & warm up camera sensor
				print("[INFO] starting video stream...")
				vs = VideoStream(usePiCamera=True).start()
				time.sleep(2.0)									# Allow video to stabalise
				cv2.namedWindow(winName)
				cv2.moveWindow(winName, 20,20)
								
				## Loop over the frames from the video stream #
				## Time-Out after 35 secs ##
				while time.time()-init_time < 35:
					## grab the frame from the threaded video stream and r
					## resize it to have a maximum width of 400 pixels
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
				 
						## Indicate Which barcode is found ##
						if staffKit == 0:
							staffKit = 1						# toggle to staff
							text = "- KIT ID -"
						else:
							staffKit = 0						# toggle back to kit
							text = "- STAFF ID -"
						
						cv2.putText(frame, text, (x, y - 10),
							cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
							
						## REMOVED - Store QR Data to CSV file ##
						
						## Count QR Reads ##
						scnCnt += 1	
						
						## If QR Code is Read 3 times ##
						if scnCnt == 5:
							#scnCnt = 0							# clear the counter
							if done == "kit":
								qrData = barcodeData			# Copy QR Data
								done = "staff"					# exit the loop
							elif done == "staff":
								staffID = barcodeData			# store staff_ID
								done = "y" 						# exit scan mode
							################################
							## PAUSE AND CHANGE INDICATOR ##
							################################
							font = cv2.FONT_HERSHEY_SIMPLEX
							text = "DONE!!"
							textsize = cv2.getTextSize(text, font, 1, 2)[0]
							
							## Get coords based on boundry ##
							textX = (frame.shape[1] - textsize[0]) /2
							textY = (frame.shape[0] - textsize[1]) /2
							
							## Add text centered in image ##
							cv2.putText(frame, text, (textX, textY), font, 2, (0, 255, 0), 3)

					## FOR FULL SCREEN ? ? - FIX ##
					#cv2.namedWindow(winName, cv2.WINDOW_NORMAL)# create a named window
					#cv2.namedWindow(winName)
					#cv2.moveWindow(winName, 20,20)				# set window placement
					## Get window to full screen ##
					#cv2.setWindowProperty(winName, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN) 
					
					## Show the output frame ##
					cv2.imshow(winName, frame)
					key = cv2.waitKey(1) & 0xFF
					
					# Pause for QR swap ##
					if scnCnt == 5:
						time.sleep(3)		
						scnCnt = 0	
				 
					## if the `q` key was pressed, break from the loop ##
					if key == ord("q"):
						break
					## if ID confirmed 3 times ##
					elif done == "y":
						#print(qrData)							# REMOVE
						#print(staffID)							# REMOVE
						break
				
				## close the output CSV file do a bit of cleanup ##
				print("[INFO] cleaning up...")
				"""
				## Impossible to Destroy Video Window ##
				cv2.waitKey(0)
				vs.stop()
				cv2.destroyWindow(winName)						# destroy specific window??
				for i in range (1,5):
					cv2.waitKey(1)
				win.destroy()
				"""
				vs.stop()										# stop video stream
				cv2.destroyAllWindows()							# NOT destroying??
				lift_window()									# Put GUI on the top
				
			
			#####################
			## GESTURE COUNTER ##
			#####################
			def get_gesture():
				global Cnt					# Double defined?
				global GestDone				# Exit Gesture flag
				Cnt = 0						# Double defined?
				direct = 'none'				# Direction of swipe
				## Temporary? ##
				GestDone = False			# 
				sendCnt = 0					# 
				
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
						
					print("CAPTURE GESTURES:")						# remove
					print("=================")						# remove
					apds.enableGestureSensor()
					while True:
						time.sleep(0.5)
						if apds.isGestureAvailable():
							motion = apds.readGesture()
							direct = dirs.get(motion, "unknown")
							#print("Gesture = {}".format(direct))	# remove
							
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
							
							## ON EVERY COUNT ##
							handleData(Cnt, sendCnt)
							sendCnt += 1
							if sendCnt == 3:
								sendCnt = 0
							
				## Do before exiting Gesture Mode ##
				finally:
					## Zero Counter - On Next Count ##
					Cnt = 0 								# zero the count value
					update_label()							# update the GUI label


			## Initialise both Threads (not started yet) ##
			threads = []										# create thread list
			thr1 = 0											# thread 1 flag
			thr2 = 0											# thread 2 flag
			
			##############################
			## BUTTON: EMPLOYEE ID SCAN ##
			##############################
			def btn_start():
				## Gesture counter #
				global GestDone								# Exit Gesture mode flag
				global thr1									# thread flag
				global Cnt									# make global again?
				## ID Scanner #
				global thr2
				global btn_state1							# changed top tri-state
				global info
				## GCP JSON ##
				global qrData								# Pass QR Code data to JSON creator
				global iotJSON								# Convert to JSON & publish

				
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
					bigButton["text"] = "START\nCOUNT"		# Change Button Title
					
					## Update GUI Info Tab ##
					info = "Info: Video Window Starting..."
					update_label()
					## If thread not started (can't start twice?)
					if thr2 == 0:
						thr2 = 1							# toggle flag
						t2.start()							# start QR Reader thread

					btn_state1 = 1							# To "START COUNTER"
					
				## START COUNT ROUTINE #
				elif btn_state1 == 1:
					print("START COUNTING ROUTINE NOW...")	# REMOVE
					
					bigButton["text"] = "STOP\nCOUNT"		# button label change
					info = "Info: Started Counting..."		# User info
					Cnt = 0									# zero counter
					
					## If thread not started (can't start twice?)
					if thr1 == 0:
						print("start gesture thread")
						thr1 = 1							# toggle flag
						t1.start()							# start gesture thread
					
					## Update GUI information ##
					update_label()
					
					btn_state1 = 2							# To "STOP COUNTER"
				
				## END COUNT ROUTINE #
				elif btn_state1 == 2:
					print("STOP COUNT")						# REMOVE
					bigButton["text"] = "START\nCOUNT"
					info = "Info: Counting Complete"
					
					## If thread was started ##
					if thr1 == 1:							# Can't start thread again? - REMOVE?
						thr1 = 0							# Clear thread flag
						GestDone = True						# Break out of Gesture funtion
						## Close the thread ##
						#t1.join()							# ERROR - reference
						
						## Update GUI information ##
						update_label()
					
					btn_state1 = 1							# Back to "START COUNTER"
			
			
			################################
			## CREATE JSON DATA STRUCTURE ##
			## PUBLISH TO GCP VIA MQTT	  ##
			################################
			def handleData(Cnt, sendCnt):
				global qrData									# QR Data to create JSON string
				global iotJSON									# returned JSON string
				
				print("PCB: {}".format(Cnt))					# REMOVE
				
				## On every 3rd count 	 ##
				## Avoid over-publishing ##
				if sendCnt == 2:
					# JSON update - [count]
					
					iotJSON = createJSON(qrData, Cnt)			# Convert to JSON format
					print("JSON Created...")					# REMOVE
					#print("{}".format(iotJSON)) 				# REMOVE
					
					#print("Publish GCP!")						# REMOVE
					iot_publish(iotJSON)						# Publish JSON Data
					print("PUBLISHED...")						# REMOVE
			
			
			####################################
			## DATA CLASS FOR JSON CONVERSION ##
			####################################
			class OmniData:
				CLIENT 	= 'TSE'
				PROJECT = 515151515
				STAGE 	= 'NULL'
				BOARDS 	= 0
				PANELS 	= 0
				STAFF_ID = 000
				DATE 	= '01-01-2020'
				TIME 	= '00:00'
				START 	= '00:00'
				STOP 	= '00:00'
				REASON 	= 'NULL'
				SERIAL 	= 121212121


			##################################
			## UPDATE ALL INFO DATA 		## 
			## CREATE JSON STRING AND STORE	## 
			##################################
			def createJSON(qrData, Cnt):
				global firstScan									# only store certain data on first scan
				global projectStat									# project start or stop
				global staffID										# Extracted Staff ID from QR Scan2
				global dataDict
				global staffKit										# kitID[0] OR staffID[1]
												
				## Get Startup Information - Time & Date on 'SETUP' stage ##
				now = datetime.datetime.now()						# Get 'nows' date & time
				#current_date = now.strftime("%Y-%m-%d")			# Extract date
				current_time = now.strftime("%H:%M:%S")				# Extract time
				
				
				
				## Update only on 1st QR Scan ##
				if firstScan == 0:
					## Extract data with ',' delimiter - Directly into Global Disctionary ##
					dataDict = dict(i.split('=') for i in qrData.split(','))
					firstScan = 1									# RETURN TO '0' EVERY TIME SCAN IS OPENED 
					current_date = now.strftime("%Y-%m-%d")			# Extract date
					dataDict['STAFF_ID'] = staffID						# Update Staff ID		- on startup
					dataDict['DATE'] = current_date					# insert current date
					dataDict['TIME'] = current_time					# insert current date

				## Depending on KIT or STAFF qrScan ##
				dataDict['START'] = current_time					# insert current time
				dataDict['STOP']  = current_time					# insert current time

				## Continuously Update PCB Value ##
				dataDict['BOARDS'] = Cnt							# Update board count 	- every count

				## Mirror dictionary data to data class ##
				## EDIT: Use loop to import new data ##
				OmniData1 = OmniData()								# get object characteristics
				OmniData1.CLIENT 	= dataDict['CLIENT']
				OmniData1.PROJECT 	= dataDict['PROJECT']
				OmniData1.STAGE 	= dataDict['STAGE']
				OmniData1.BOARDS 	= dataDict['BOARDS']
				OmniData1.PANELS 	= dataDict['PANELS']
				OmniData1.STAFF_ID 	= dataDict['STAFF_ID']
				OmniData1.DATE 		= dataDict['DATE']
				OmniData1.TIME 		= dataDict['TIME']
				OmniData1.START 	= dataDict['START']
				OmniData1.STOP 		= dataDict['STOP']
				OmniData1.REASON 	= dataDict['REASON']
				OmniData1.SERIAL 	= dataDict['SERIAL']

				## Convert Data Class to JSON string ##
				## NOTE: Data fields are not created in the same order ##
				jsonStr = json.dumps(OmniData1.__dict__)

				## Pass JSON string back ##
				return jsonStr
			
			
			##############################
			## CREATE THE JWT TOKEN KEY ##
			##############################
			def create_jwt():
				token = {
					'iat': cur_time,
					'exp': cur_time + datetime.timedelta(minutes=60),
					'aud': project_id
				}
				
				with open(ssl_private_key_filepath, 'r') as f:
					private_key = f.read()
					
				return jwt.encode(token, private_key, ssl_algorithm)
			
			
			##################################
			## CONNECT VIA MQTT AND PUBLISH ##
			##################################
			def iot_publish(iotJSON):
				_CLIENT_ID = 'projects/{}/locations/{}/registries/{}/devices/{}'.format(project_id, gcp_location, registry_id, device_id)
				_MQTT_TOPIC = '/devices/{}/events'.format(device_id)

				client = mqtt.Client(client_id=_CLIENT_ID)
				# authorization is handled purely with JWT, no user/pass, so username can be whatever
				client.username_pw_set(
					username='unused',
					password=create_jwt())

				def error_str(rc):
					return '{}: {}'.format(rc, mqtt.error_string(rc))

				def on_connect(unusued_client, unused_userdata, unused_flags, rc):
					print('on_connect', error_str(rc))

				def on_publish(unused_client, unused_userdata, unused_mid):
					print('on_publish')

				client.on_connect = on_connect
				client.on_publish = on_publish

				client.tls_set(ca_certs=root_cert_filepath) # Replace this with 3rd party cert if that was used when creating registry
				client.connect('mqtt.googleapis.com', 8883)
				client.loop_start()
				
				"""
				## Single Publish ##
				payload = iotJSON
				## Actually publish the Data ## 
				client.publish(_MQTT_TOPIC, payload, qos=1)
				## View the payload data ##
				print("{}\n".format(payload))				
				time.sleep(1)
				client.loop_stop()
				"""
				
				## Multiple Publishes to IoT Core (~Twice~) ##
				for i in range(1, 3):
					payload = iotJSON							# move data to payload
					
					## Actually publish the Data ## 
					client.publish(_MQTT_TOPIC, payload, qos=1)
					print("{}\n".format(payload))				# REMOVE			
					
					time.sleep(1)								# REQUIRED ? ?
					client.loop_stop()							# Close loop
				

			############################
			# DROP DOWN MENU CALLBACK ##
			############################
			def callback(*args):
				global info 
		
				# Update info bar in 'main.py'
				info = "Info: stage - {}".format(dropD.get())	# New 'info' message
				update_label()									# Update GUI Info label
				
				## Begin Exit Routine ##
				if dropD.get() == "EXIT":
					exitProgram()
				## Update Stage to Dictionary ##
				else:
					dataDict['STAGE'] = dropD.get()
			
			
			###########################
			## REALTIME LABEL UPDATE ##
			###########################
			def update_label():
				global Cnt
				global info
				
				## Update Count Label ##
				label_4.config(text="- {} -".format(Cnt), font = myFont1)
				## Update Info Label ##
				label_6.config(text="{}".format(info), font = "Helvetica 10")
			
			
			#########################
			## BRING WINDOW TO TOP ##
			#########################
			def lift_window():
				print("Lift Window")
				win.lift()
			
			
			###############################
			## NUMERICAL EXIT CODE ENTRY ##
			###############################
			def code(value):
				global pin									# 
				global ExCode								# 

				## '*' Key presses ##
				if value == '*':
					## remove last digit from `pin` ##
					pin = pin[:-1]
				
				## '#' Key presses ##
				elif value == '#':
					## check pin ##
					if pin == "3529":						# Set pin number here!
						print("PIN OK")						# console - REMOVE
						pin = ''							# clear `pin`
						#ExCode = True 						# Set ExCode
						KeyPadExit(True)					# Close keypad window
					else:
						print("INCORRECT PIN!")				# console - REMOVE
						pin = ''							# clear `pin`
						
						# After 3 attempts - Close keypad window
						KeyPadExit(False)					# must be repeatable

				## Any digit keys pressed ##
				else:
					pin += value							# Add digit to pin
				
				print("Current: " + pin)					# show input code
			
			
			##########################
			## CREATE KEYPAD WINDOW ##
			##########################
			def KeyPadWin():
				## Define keypad keys ##
				keys = [
					['1', '2', '3'],    
					['4', '5', '6'],    
					['7', '8', '9'],    
					['*', '9', '#'],    
				]
				## Create new Window ##
				keyPadWin = Toplevel(win)
				lay.append(keyPadWin)
				keyPadWin.title("EXIT CODE")
				
				## Create buttons using `keys`
				for y, row in enumerate(keys, 1):
					for x, key in enumerate(row):
						# `lambda` inside `for` has to use `val=key:code(val)` 
						# instead of direct `code(key)`
						b = Button(keyPadWin, text=key, command=lambda val=key:code(val))
						b.grid(row=y, column=x, ipadx=10, ipady=10)
			
			
			########################
			## EXIT KEYPAD WINDOW ##
			########################
			def KeyPadExit(CodeDone):
				global info										# App information
				
				print("[INFO] Destroy Window...")			# REMOVE
				keyPadWin = lay[0]								# DON'T THINK THIS WORKING??
				
				if CodeDone == True:
					print("[INFO] Quit Main Program!!")		# REMOVE
					## Destroy All Windows ##
					## NOT DESTROYING CV2 WINDOW ? ? ##
					win.quit()
					win.destroy()
					sys.exit(0)
				else:
					## Info: Exit Failed ##
					info = "Info: Exit Code Incorrect"			# New 'info' message
					update_label()								# Update GUI Info label 
					print("[INFO] Exit Code Incorrect")		# REMOVE
						
					## Destroy Keypad Window ##
					keyPadWin.destroy()							
					keyPadWin.update()							# --- Only works once? ? ?
			
			
			##########################
			## EXIT AND DESTROY GUI ##
			##########################
			def exitProgram():
				global thr1										# Thread exitted correctly
				global info										# App information
				global ExCode									# code correct/incorrect - flag
				
				ExCode = False									# Normally Blocked
				
				## Check thread ended properly ##
				if thr1 == 0:
					## Enter Exit Code ##
					KeyPadWin()									# keypad input
				else:
					print("Still busy...")						# console - REMOVE


			## INITIALISE NEW WINDOW ##
			win = Tk()
			## Define the Fonts:
			myFont1 = tkFont.Font(family = 'Helvetica', size = 30, weight = 'bold')
			myFont2 = tkFont.Font(family = 'Helvetica', size = 12, weight = 'bold')

			# SETUP WINDOW PARAMTERS ##
			win.title("OMNIGO")							# define window title
			win.geometry('480x320+0+0')					# define screen size	- swap
			#win.attributes("-fullscreen", True)		# full screen GUI		- swap
			win.configure(background = "gray15")		# set colour
			
			# DROP-DOWN MENU ##
			dropD = StringVar(win)
			dropD.set("Stage")

			opt = OptionMenu(win, dropD, *OptionList)
			opt.config( width=5, 
						font=('Helvetica', 10), 
						bg		= "gray15",
						fg 		= "gray64",)
			opt.pack(side="top", anchor="nw")
			
			# EXIT BUTTON - REMOVED ##
			
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
			bigButton.pack(anchor=CENTER)				# place the object
				
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
			label_5.pack(padx=10)						# spcer from button
			label_4.pack(padx=10)						# PCB counter
			label_6.pack(anchor=SW)						# PCB counter
			
			# DROP-DOWN Function Call ##
			dropD.trace("w", callback)
			
			# GUI main loop ##
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
