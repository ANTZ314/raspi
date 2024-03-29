# -*- coding: utf-8 -*-
"""
Description:
Tkinter based 3 button GUI test

USAGE:
python gui2.py
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
			
			def btn_scan():
				print("BUTTON 1 PRESSED")
				global btn_state1
				if btn_state1 == 0:
					scanButton["text"] = "SCAN ON"
					btn_state1 = not btn_state1
					
				else:
					scanButton["text"] = "SCAN OFF"
					btn_state1 = not btn_state1
			
			def btn_cnt():
				print("BUTTON 2 PRESSED")
				global btn_state2
				if btn_state2 == 0:
					cntButton["text"] = "COUNT ON"
					btn_state2 = not btn_state2
					
				else:
					cntButton["text"] = "COUNT OFF"
					btn_state2 = not btn_state2
			
			def exitProgram():
				print("Exit Button pressed")
				win.quit()
			
			win = Tk()

			myFont = tkFont.Font(family = 'Helvetica', size = 24, weight = 'bold')

			win.title("OMNIGO")
			win.geometry('480x320')

			exitButton  = Button(win, text = "Exit", font = myFont, command = exitProgram, height =1 , width = 5) 
			exitButton.pack(side = BOTTOM)

			scanButton = Button(win, text = "SCAN", font = myFont, command = btn_scan, height = 3, width = 10)
			scanButton.pack(side = LEFT)
			
			cntButton = Button(win, text = "COUNT", font = myFont, command = btn_cnt, height = 3, width = 10)
			cntButton.pack(side = RIGHT)

			mainloop()

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
