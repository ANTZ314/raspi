# -*- coding: utf-8 -*-
"""
Description:
Tkinter based 3 button GUI test with camera module
Edited for random testing...

USAGE:
python gui5.py
"""
######################
## IMPORT LIBRARIES ##
######################
from Tkinter import *
import tkFont
from picamera import PiCamera
from time import sleep
import traceback

#####################
##   GLOBAL DEFS   ##
#####################
btn_state1 = True
btn_state2 = True


#####################
##  MAIN FUNCTION  ##
#####################
def main():
	try:
		try:
			global Cnt					# make global variable
			Cnt = 13					# returned number of PCB's
			camera = PiCamera()			# camera test
			
			def btn_scan():
				print("BUTTON 1 PRESSED")
				global btn_state1
				#global camOn
				
				if btn_state1 == False:
					print("Camera Test...")
					camera.start_preview()
					sleep(5)
					camera.stop_preview()
				
					scanButton["text"] = "SCAN ON"
					btn_state1 = not btn_state1
					
				else:
					scanButton["text"] = "SCAN OFF"
					btn_state1 = not btn_state1
			
			def btn_cnt():
				print("BUTTON 2 PRESSED")
				global btn_state2
				global Cnt						# make global again?
				
				if btn_state2 == False:
					Cnt += 1					# increment counter
					print("Counter: {}".format(Cnt))
					label_4.config(text="Count: {}".format(Cnt), font = "Helvetica 12")
					
					cntButton["text"] = "COUNT 1"
					btn_state2 = not btn_state2
					
				else:
					Cnt += 1					# increment counter
					print("Counter: {}".format(Cnt))
					label_4.config(text="Count: {}".format(Cnt), font = "Helvetica 12")
					
					cntButton["text"] = "COUNT 2"
					btn_state2 = not btn_state2
			
			def exitProgram():
				print("Exit Button pressed")
				win.quit()
			
			# Create the window
			win = Tk()

			# Create reusable font
			myFont = tkFont.Font(family = 'Helvetica', size = 24, weight = 'bold')

			# Window title and dimensions
			win.title("OMNIGO")
			win.geometry('480x320')
			win.configer(background="darkblue")
			
			# Spacer
			label_1 = Label(win, text="   ", font = "Helvetica 10")
			# Main Title
			label_2 = Label(win, 
							text 	= "- OMNIGO -", 
							relief 	= "solid",
							font 	= "Times 24",
							width 	= 11,
							height	= 1)
			# Spacer
			label_3 = Label(win, text="   ", font = "Helvetica 10")
			# PCB Count
			label_4 = Label(win, text="Count: {}".format(Cnt), font = "Helvetica 12")
			
			label_1.pack()
			label_2.pack()
			label_3.pack()
			label_4.pack()

			# EXIT BUTTON
			exitButton  = Button(win, 
								text = "Exit", 
								font = myFont, 
								command = exitProgram, 
								height =1 , 
								width = 5) 
			exitButton.pack(side = BOTTOM)

			# ID SCAN BUTTON
			scanButton = Button(win, 
								text = "SCAN", 
								font = myFont, 
								command = btn_scan,
								fg = "darkgreen",
								bg = "white",
								height = 3, 
								width = 10)
			scanButton.pack(side = LEFT)
			
			# COUNT BUTTON
			cntButton = Button(win, 
								text = "COUNT", 
								font = myFont, 
								command = btn_cnt,
								fg = "darkgreen",
								bg = "white",
								height = 3, 
								width = 10)
			cntButton.pack(side = RIGHT)

			mainloop()
			
		# Ctrl+C will exit the program correctly
		except KeyboardInterrupt:
			print("Keyboard Interupt - EXIT")
			sys.exit(0)
		
	# Any Main Errors saved to log.txt file:
	except Exception:
		print("Exception reached - Check Log.txt File")
		log = open("log.txt", 'w')
		traceback.print_exc(file=log)
		sys.exit(0)


if __name__ == "__main__":	main()
