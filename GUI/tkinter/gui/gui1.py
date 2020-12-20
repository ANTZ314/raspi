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
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(40, GPIO.OUT)
GPIO.output(40, GPIO.LOW)



#####################
##  MAIN FUNCTION  ##
#####################
def main():	
	try:
		try:
			
			def ledON():
				print("LED button pressed")
				if GPIO.input(40) :
					GPIO.output(40,GPIO.LOW)
					ledButton["text"] = "LED ON"
				else:
					GPIO.output(40,GPIO.HIGH)
					ledButton["text"] = "LED OFF"

			def exitProgram():
				print("Exit Button pressed")
				GPIO.cleanup()
				win.quit()
			
			win = Tk()

			myFont = tkFont.Font(family = 'Helvetica', size = 36, weight = 'bold')

			win.title("First GUI")
			win.geometry('800x480')

			exitButton  = Button(win, text = "Exit", font = myFont, command = exitProgram, height =2 , width = 6) 
			exitButton.pack(side = BOTTOM)

			ledButton = Button(win, text = "LED ON", font = myFont, command = ledON, height = 2, width =8 )
			ledButton.pack()

			mainloop()

			#print("DONE!!")					# Guess what this does??
			#sys.exit(0)						# exit properly
			
		# Ctrl+C will exit the program correctly
		except KeyboardInterrupt:
			print("Keyboard Interupt - EXIT")
			GPIO.cleanup()
			sys.exit(0)
		
	# Any Main Errors saved to log.txt file:
	except Exception:
		print("Exception reached - Check Log.txt File")
		log = open("log.txt", 'w')
		traceback.print_exc(file=log)
		GPIO.cleanup()
		sys.exit(0)


if __name__ == "__main__":	main()
