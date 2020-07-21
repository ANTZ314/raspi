#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Description:
* Tkinter GUI with threading for continuous button use
* Testing thread restarting after destroyed
* apparently don't destroy in the first place??

USAGE:
python gui11.py
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

from picamera import PiCamera			# Testing the Camera
import threading						# Multi-threading

###################
##  GLOBAL DEFS  ##
###################
## Buttons
btn_state2 = True


###################
## MAIN FUNCTION ##
###################
def main():
	global thr										# thread flag
	global CamWin									# kill the camera thread
	
	
	## Main Exception ##
	try:
		## Keyboard Interrupt ##
		try:
			###################
			## TEST FUNCTION ##
			###################
			def testfunc():
				global Cnt							# global counter
				global CamWin						# thread loop flag
				
				CamWin = False
				
				print("START COUNTER...")
				Cnt = 1
				while CamWin == False:
					sleep(1)						# delay
					Cnt += 1						# increment
				print("DONE: {}".format(Cnt))		#
			
			######################
			## Intialise Thread ##
			######################
			threads = []							# create list of threads
			thr = 0
			
			## BUTTON: GESTURE COUNING ##
			def btn_cnt(PCB):
				global CamWin						# End the thread flag
				global thr							# thread flag
				global btn_state2					# toggling button state
				
				## Start new thread each time ##
				if thr == 0:
					t1 = threading.Thread(target=testfunc)	# Not started yet
					threads.append(t1)						# for multiple threads
				
				## Click1 ##
				if btn_state2 == False:
					cntButton["text"] = "STOP\nCAMERA"
					## If thread not started ##
					if thr == 0:					# Can't start twice? ? ?
						thr = 1						# toggle flag
						t1.start()					# start gesture thread
						print("start thread")
					
					btn_state2 = not btn_state2		# toggle button flag
				
				## Click2 ##
				else:
					cntButton["text"] = "START\nCAMERA"
					## If thread was started ##
					if thr == 1:					# Can't start thread again? - REMOVE?
						print("END THREAD")
						thr = 0						# Clear thread flag
						CamWin = True				# Exit counter loop
						## Close the thread ##
						#t1.join()					# ERROR - ref before defined
					btn_state2 = not btn_state2		# toggle button flag
			
			
			## EXIT BUTTON ##
			def exitProgram():
				print("- GOODBYE -")
				## If thread not already ended ##
				if thr == 1:
					## Close the thread ##
					t1.join()
				win.quit()
			
			## Initialise the Window ##
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
							text	= "Count: {}".format(13), 
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
