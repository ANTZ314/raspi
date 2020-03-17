#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Description:
To be able to access label continuously for real time board count display:
-> First used test thread with global count value to update label
-> Next move "get_gesture()" to main

USAGE:
python gui6.py
"""
###################
# import packages #
###################
from Tkinter import *					# GUI package
import tkFont							# GUI package
from functools import partial			# passing argument to button?
import sys, time						# Possibly remove ? ?
from time import sleep					# Delays
import traceback						# Error logging

## GESTURE IMPORTS ##
from apds9960.const import *			# Gesture sensor library
from apds9960 import APDS9960			# Gesture sensor library
import smbus							# Something to do with SPI port ? ?

import threading

###################
##  GLOBAL DEFS  ##
###################
## Buttons
btn_state2 = True

## Gesture Sensor Requirements
port = 1
bus  = smbus.SMBus(port)
apds = APDS9960(bus)

######################
## GESTURE FUNCTION ##
######################
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
				print("Gesture = {}".format(direct))
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
				
				# change the value on the GUI - ERROR?
				#label_4.config(text="Count: {}".format(brd_cnt), font = "Helvetica 12")
				print("PCB Count: {}".format(Cnt))
				
				# Increment exit counter - REMOVE 
				exitCnt += 1				
			# After 'x' swipes - REMOVE 
			if exitCnt == 7:
				GestDone = True
			
			# Break from loop early
			if GestDone == True:
				break
	finally:
		print ("Final Board Count: {}".format(Cnt))

###################
## MAIN FUNCTION ##
###################
def main():
	global thr										# thread flag
	global Cnt										# PCB count value
	global GestDone									# Exit Gesture mode flag
	
	GestDone = False
	Cnt = 0											# random start value
	
	## Main Exception
	try:
		###################
		## TEST FUNCTION ##
		###################
		def testfunc():
			global Cnt
			global GestDone							# test loop function - REMOVE?
			
			print("START COUNTER...")
			while GestDone == False:
				print("BOARD: {}".format(Cnt))		# show board count
				update_label()
				sleep(1)							# delay
				Cnt += 1							# increment
			print("DONE: {}".format(Cnt))
		
		## Intialise Gesture Thread (not started yet)
		#t1 = threading.Thread(target=get_gesture)
		t1 = threading.Thread(target=testfunc)		# Test function - REMOVE
		thr = 0
		
		## Keyboard Interrupt
		try:
			## BUTTON: GESTURE COUNING ##
			def btn_cnt(PCB):
				global GestDone						# Exit Gesture mode flag
				global thr							# thread flag
				global btn_state2					# toggling button state
				global Cnt							# make global again?
				
				## Click1
				if btn_state2 == False:
					cntButton["text"] = "STOP\nCOUNT"
					## If thread not started (can't start twice?)
					if thr == 0:
						thr = 1						# toggle flag
						t1.start()					# start gesture thread
					
					## Update initial count value
					## -> REDUNDANT: Unless continuing count
					update_label()
					
					btn_state2 = not btn_state2		# toggle button flag
				
				## Click2
				else:
					cntButton["text"] = "START\nCOUNT"
					## If thread was started
					if thr == 1:					# Can't start thread again? - REMOVE?
						thr = 0						# Clear thread flag
						GestDone = True				# Break out of Gesture funtion
						## Close the thread
						t1.join()					# Close the thread
						#print("Count Returned: {}".format(Cnt))	# confirmation - REMOVE?
						
						## Show the final count on the GUI
						update_label()
					
					btn_state2 = not btn_state2		# toggle button flag
			
			## Update Count Value to the label ##
			def update_label():
				global Cnt
				# Change label
				label_4.config(text="Count: {}".format(Cnt), font = myFont2)
			
			## EXIT BUTTON ##
			def exitProgram():
				print("- GOODBYE -")
				if thr == 1:
					## Close the thread
					t1.join()
				win.quit()
			
			## Initialise the Window
			win = Tk()

			## Define the Fonts:
			myFont1 = tkFont.Font(family = 'Helvetica', size = 24, weight = 'bold')
			myFont2 = tkFont.Font(family = 'Helvetica', size = 12, weight = 'bold')

			## Define Window Features
			win.title("OMNIGO")						# Window heading
			#win.attributes("-fullscreen", True)	# Full Screen
			win.geometry("480x320+0+0")				# Set size & position
			win.configure(background = "darkblue")	# Background colour
			
			## Spacer
			label_1 = Label(win, 
							text	= " ",
							bg 		= "darkblue",
							font 	= "Helvetica 10")
			## Main Title
			label_2 = Label(win, 
							text 	= "- OMNIGO -", 
							bg 		= "darkblue",
							relief 	= "solid",
							font 	= "Times 24",
							width 	= 11,
							height	= 1)
			## Spacer
			label_3 = Label(win, 
							text	= " ", 
							bg 		= "darkblue",
							font 	= "Helvetica 10")
			## PCB Count
			label_4 = Label(win, 
							text	= "Count: {}".format(Cnt), 
							fg 		= "white",
							bg 		= "darkblue",
							font 	= "Helvetica 14")
			
			label_1.pack()
			label_2.pack()
			label_3.pack()
			label_4.pack()

			## EXIT BUTTON
			exitButton  = Button(win, 
								text 	= "Exit", 
								font 	= myFont1, 
								command = exitProgram, 
								height 	= 1 , 
								width 	= 5) 
			exitButton.pack(side = BOTTOM)

			
			## COUNT BUTTON
			cntButton = Button(win, 
								text 	= "CLICK ME", 
								font 	= myFont1, 
								command = partial(btn_cnt, 5),
								fg 		= "darkgreen",
								bg 		= "white",
								height 	= 3, 
								width 	= 10)
			cntButton.pack()
			
			mainloop()
			
		## Ctrl+C will exit the program correctly
		except KeyboardInterrupt:
			print("main.py - keyboard interupt")
			sys.exit(0)
		
	## Any Main Errors saved to log.txt file:
	except Exception:
		print("main.py - Exception reached")
		log = open("log.txt", 'w')
		traceback.print_exc(file=log)
		sys.exit(0)


if __name__ == "__main__":	main()
