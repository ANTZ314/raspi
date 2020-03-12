#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Description:
Single button Tkinter Threading Test - works
Basic test with counter loop function running as thread	
2nd click stops thread.
Thread will not initiate a 2nd time
NOT RETURNING THE COUNT VALUE?? - line 86

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

import threading

###################
##  GLOBAL DEFS  ##
###################
btn_state1 = True
btn_state2 = True

###################
## TEST FUNCTION ##
###################
def testfunc(Cnt):
	global looper								# test loop function
	
	print("START COUNTER...")
	while looper == True:
		print("BOARD: {}".format(Cnt))			# show board count
		sleep(1)								# delay
		Cnt += 1								# increment
	print("Return {}".format(Cnt))
	return Cnt

###################
## MAIN FUNCTION ##
###################
def main():
	global looper		# test loop function
	global thr									# thread flag
	pcb_cnt  = 0								# number of PCB's counted
	global Cnt									# make global variable
	Cnt = 13									# returned number of PCB's
	
	thr = 0
	t1 = threading.Thread(target=testfunc, args=(Cnt,))
	looper = True
	
	try:
		try:
			## BUTTON: GESTURE COUNING ##
			def btn_cnt(PCB):
				global looper					# test loop function
				global thr						# thread flag
				global btn_state2				#
				global Cnt						# make global again?
				
				if btn_state2 == False:
					# If thread not started
					if thr == 0:
						thr = 1					# toggle flag
						t1.start()				# start gesture thread
					
					# Show the final count on the GUI
					label_4.config(text="Count: {}".format(Cnt), font = myFont2)
					
					cntButton["text"] = "STOP\nCOUNT"
					btn_state2 = not btn_state2
					
				else:
					cntButton["text"] = "START\nCOUNT"
					if thr == 1:
						looper = False
						## NOT RETURNING THE COUNT VALUE??
						Cnt = t1.join()
						thr = 0
						print("Count: {}".format(Cnt))
						# Show the final count on the GUI
						label_4.config(text="Count: {}".format(Cnt), font = myFont2)
					
					btn_state2 = not btn_state2
			
			def exitProgram():
				print("Exit Button Pressed")
				if thr == 1:
					Cnt = t1.join()
				win.quit()
			
			# Initialise the Window
			win = Tk()

			# Define the Fonts:
			myFont1 = tkFont.Font(family = 'Helvetica', size = 24, weight = 'bold')
			myFont2 = tkFont.Font(family = 'Helvetica', size = 12, weight = 'bold')

			# Define Window Features
			win.title("OMNIGO")						# Window heading
			#win.attributes("-fullscreen", True)	# Full Screen
			win.geometry("480x320+0+0")				# Set size & position
			win.configure(background = "darkblue")	# Background colour
			
			# Spacer
			label_1 = Label(win, 
							text	= " ",
							bg 		= "darkblue",
							font 	= "Helvetica 10")
			# Main Title
			label_2 = Label(win, 
							text 	= "- OMNIGO -", 
							bg 		= "darkblue",
							relief 	= "solid",
							font 	= "Times 24",
							width 	= 11,
							height	= 1)
			# Spacer
			label_3 = Label(win, 
							text	= " ", 
							bg 		= "darkblue",
							font 	= "Helvetica 10")
			# PCB Count
			label_4 = Label(win, 
							text	= "Count: {}".format(Cnt), 
							fg 		= "white",
							bg 		= "darkblue",
							font 	= "Helvetica 14")
			
			label_1.pack()
			label_2.pack()
			label_3.pack()
			label_4.pack()

			# EXIT BUTTON
			exitButton  = Button(win, 
								text 	= "Exit", 
								font 	= myFont1, 
								command = exitProgram, 
								height 	= 1 , 
								width 	= 5) 
			exitButton.pack(side = BOTTOM)

			
			# COUNT BUTTON
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
