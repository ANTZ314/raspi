# -*- coding: utf-8 -*-
"""
Description:
Tkinter based button GUI test
Full screen window

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



#####################
##  MAIN FUNCTION  ##
#####################
def main():	
	try:
		try:
			
			def fck_btn():
				#print("BUTTON 1 PRESSED")
				global btn_state1
				if btn_state1 == 0:
					ledButton["text"] = "FUCK YOU"
					btn_state1 = not btn_state1
					
				else:
					ledButton["text"] = "AND YOUR MOM"
					btn_state1 = not btn_state1

			def exitProgram():
				print("OUT!!")
				win.quit()
			
			win = Tk()

			myFont = tkFont.Font(family = 'Helvetica', size = 36, weight = 'bold')

			#win_width  = win.winfo_screenwidth()
			#win_height = win.winfo_screenheight()

			win.title("FUCKER")
			win.attributes("-fullscreen", True)
			#win.geometry("%dx%d+0+0" % (win_width, win_height))
			#win.geometry('800x480')
			win.configure(background = "darkblue")

			# Spacer
			label_1 = Label(win, text="", font = "Helvetica 10")
			label_1.pack()

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

			# ID SCAN BUTTON
			ledButton = Button(win, 
								text = "TRY ME", 
								font = myFont, 
								command = fck_btn,
								fg = "lightgreen",
								bg = "black",
								height = 5, 
								width = 15)
			#ledButton.pack(side = LEFT)
			ledButton.pack()
			
			# Spacer
			#label_2 = Label(win, text="spacer", font = "Helvetica 10")
			#label_2.pack(side = BOTTOM)
			
			
			win.mainloop()

			#print("DONE!!")					# Guess what this does??
			#sys.exit(0)						# exit properly
			
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
