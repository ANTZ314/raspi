# -*- coding: utf-8 -*-
"""
Description:
Tkinter based button GUI test

USAGE:
python gui1.py
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
btn_state1 = 0
btn_state2 = 0

camera = PiCamera()

#####################
##  MAIN FUNCTION  ##
#####################
def main():	
	try:
		try:
			
			def fck_btn():
				global btn_state1
				if btn_state1 == 0:
					ledButton["text"] = "SCAN"
					label_2.config(text="THE TEST NEVER LIES...")
					btn_state1 = not btn_state1
					
				else:
					ledButton["text"] = "CUTEY!"
					btn_state1 = not btn_state1
					
					print("SCANNING FOR PEOPLE...")
					label_2.config(text="-FOUND A GORGEOUS GIRL-")
					sleep(2)
					camera.start_preview()
					sleep(4)
					camera.stop_preview()
					camera.close()

			def exitProgram():
				print("OUT!!")
				win.quit()
			
			win = Tk()

			myFont = tkFont.Font(family = 'Helvetica', size = 36, weight = 'bold')
			myFont2 = tkFont.Font(family = 'Helvetica', size = 24, weight = 'bold')

			win.title("First GUI")
			win.geometry('480x320')					# 
			#win.attributes("-fullscreen", True)	# Full Screen
			win.configure(background = "darkblue")

			# Spacer
			label_1 = Label(win, 
							text="", 
							bg = "darkblue",
							font = "Helvetica 10")
			label_1.pack()
			
			# gay test
			label_2 = Label(win, 
							text="WELCOME TO THE PERSON SCANNER!!", 
							fg = "white",
							bg = "darkblue",
							font = "Helvetica 12")
			label_2.pack()

			# GAY BUTTON
			ledButton = Button(win, 
								text = "TRY ME", 
								font = myFont, 
								command = fck_btn,
								fg = "lightgreen",
								bg = "black",
								height = 2, 
								width = 12)
								
			#ledButton.pack(side = LEFT)
			ledButton.pack()
			
			
			# Exit button
			exitButton  = Button(win, 
								text = "Exit", 
								font = myFont, 
								command = exitProgram, 
								fg = "lightgreen",
								bg = "black",
								height =2 , 
								width = 6) 
			exitButton.pack(side = BOTTOM)
			
			mainloop()
			
		# Ctrl+C will exit the program correctly
		except KeyboardInterrupt:
			print("Keyboard Interupt - EXIT")
			#camera.close()
			sys.exit(0)
		
	# Any Main Errors saved to log.txt file:
	except Exception:
		print("Exception reached - Check Log.txt File")
		log = open("log.txt", 'w')
		traceback.print_exc(file=log)
		sys.exit(0)


if __name__ == "__main__":	main()
