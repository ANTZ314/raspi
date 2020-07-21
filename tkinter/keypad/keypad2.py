from Tkinter import *
import tkFont
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(40, GPIO.OUT)
GPIO.output(40, GPIO.LOW)

win = Tk()

myFont = tkFont.Font(family = 'Helvetica', size = 36, weight = 'bold')

def ledON():
    print("LED button pressed")
    if GPIO.input(40) :
        GPIO.output(40,GPIO.LOW)
                ledButton["text"] = "LED OFF"
    else:
        GPIO.output(40,GPIO.HIGH)
                ledButton["text"] = "LED ON"

def exitProgram():
    print("Exit Button pressed")
       GPIO.cleanup()
    win.quit()  


win.title("LED GUI")


exitButton  = Button(win, text = "1", font = myFont, command = ledON, height     =2 , width = 8) 
exitButton.pack(side = LEFT, anchor=NW, expand=YES)

ledButton = Button(win, text = "2", font = myFont, command = ledON, height = 2, width =8 )
ledButton.pack(side = TOP, anchor=CENTER, expand=YES)

ledButton = Button(win, text = "3", font = myFont, command = ledON, height = 2, width =8 )
ledButton.pack(side = RIGHT, anchor=NE, expand=YES)

ledButton = Button(win, text = "4", font = myFont, command = ledON, height = 2, width =8 )
ledButton.pack(side = TOP, anchor=W, expand=YES)

ledButton = Button(win, text = "5", font = myFont, command = ledON, height = 2, width =8 )
ledButton.pack(side = TOP, anchor=W, expand=YES)

ledButton = Button(win, text = "6", font = myFont, command = ledON, height = 2, width =8 )
ledButton.pack(side = TOP, anchor=W, expand=YES)

ledButton = Button(win, text = "7", font = myFont, command = ledON, height = 2, width =8 )
ledButton.pack(side = TOP, anchor=W, expand=YES)

ledButton = Button(win, text = "8", font = myFont, command = ledON, height = 2, width =8 )
ledButton.pack(side = TOP, anchor=W, expand=YES)

ledButton = Button(win, text = "9", font = myFont, command = ledON, height = 2, width =8 )
ledButton.pack(side = TOP, anchor=N, expand=YES)

ledButton = Button(win, text = "0", font = myFont, command = ledON, height = 2, width =8 )
ledButton.pack(side = TOP, anchor=NW, expand=YES)



mainloop()