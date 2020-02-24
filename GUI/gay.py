# -*- coding: utf-8 -*-
"""
Description:
GAY finder using picam

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
					ledButton["text"] = "FIND A GAY!"
					label_2.config(text="THE TEST NEVER LIES...")
					btn_state1 = not btn_state1
					
				else:
					ledButton["text"] = "GAY FOUND!"
					btn_state1 = not btn_state1
					
					print("FINDING GAYS...")
					label_2.config(text="OKAY, LET ME SHOW YOU ONE...")
					sleep(2)
					camera.start_preview()
					sleep(5)
					camera.stop_preview()
					camera.close()

			def exitProgram():
				print("OUT!!")
				win.quit()
			
			win = Tk()

			myFont = tkFont.Font(family = 'Helvetica', size = 36, weight = 'bold')

			win.title("First GUI")
			win.geometry('480x320')
			win.configure(background = "darkblue")

			# Spacer
			label_1 = Label(win, 
							text="", 
							bg = "darkblue",
							font = "Helvetica 10")
			label_1.pack()
			
			# gay test
			label_2 = Label(win, 
							text="WELCOME TO THE ULTIMATE GAYE TEST!!", 
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
