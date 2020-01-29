# -*- coding: utf-8 -*-
"""
Created:		A.Smith [2017-11]
Description:	Main Class
Functionality:	

"""
import ledClass as leds
import btnClass as btn
import usbClass as usb
import quitClass as quit1
import RPi.GPIO as GPIO
import sys, time, os
import picamera

## RASPI VERSION ##
path1 = "/media/pi/"												# RasPi - path to media
path2 = "/home/pi/Pictures/dropbox/"

#########################################
## VARIABLE PAUSE BTWN CAPTURED FRAMES ##
#########################################
def long_wait(check, pause):			
	if check == True:
		for x in range (int(pause)):
			time.sleep(1)		
	else:
		print("Incorrect value!")

#################
# MAIN FUNCTION #
#################
def main():
	quit_flg  = 0														# quit button flag
	store_flg = 0														# USB storage flag
	confirm = 0															# quit confirmation
	quit_conf = 0
	
	LEDS = leds.LEDClass()												# LED control class 
	BTN  = btn.btnClass()												# Push Btn class
	USB  = usb.usbClass()												# USB Storage class
	QUIT = quit1.quitClass()											# Shutdown class
	
	LEDS.All_Off1()														# LED 1 Off
	LEDS.All_Off2()														# LED 2 Off
	print "LET'S BEGIN!!"
	try:
		while True:
			###################
			## STANDBYE MODE ##
			###################
			if BTN.switch():											# if switch HIGH - ON
				###############
				## QUIT BTN: ##
				###############	
				if BTN.Btn1() == 1:										# Btn pressed
					print("STORE IMAGES TO USB!")
					for x in range(0, 3):
						LEDS.Quick_Blue1()								# Blink 3 times: indicator
					# Toggle Button Press
					quit_flg  = 0										# confirm off
					store_flg = not store_flg							# toggle flag
				
				###############
				## QUIT BTN: ##
				###############
				if BTN.Btn2() == 1:
					print("EXIT BUTTON!")
					for x in range(0, 3):
						LEDS.Quick_Blue1()								# Blink 3 times: indicator
					# Toggle Button Press
					quit_flg  = not quit_flg							# set flag
					store_flg = 0										# confirm off
					
				#######################
				## DATA STORE TO USB ##
				#######################
				if store_flg == 1:
					LEDS.Blink_Red1()
					## If NO images in folder ##
					if os.listdir(path2) == []:
						print("FOLDER EMPTY")
					else:
						## If file exists & USB dest, move to destination ##
						USB.usb_put(path1)									# Move to USB destination
						print("Moved to USB")
						exit_flag = 1
					
					# Once complete -> back to stanbye mode
					time.sleep(2)
					store_flg = not store_flg
				else:
					if quit_flg == 0:
						# Blink Violet to indicate standbye mode
						LEDS.Blink_Purple1()
					
				##############
				## SHUTDOWN ##
				##############
				if quit_flg == 1:					
					# Quit confirmed (button pressed again)
					while quit_conf < 5:
						# Blink Yellow until confirmed quit
						LEDS.Blink_Yellow1()
						if BTN.Btn2() == 1:
							for x in range(0, 3):
								LEDS.Quick_Blue1()
							confirm = 1
							break
						quit_conf += 1									# increment counter
						#time.sleep(1)									# 1 sec wait
						
					# Quit was confirmed in 10 sec
					if confirm == 1:
						LEDS.Blink_Green1()
						quit_conf = 0									# clear value
						confirm = 0										# clear value
						# Shutdown sequence
						QUIT.quit1()
						# Temporary
						GPIO.cleanup()									# Kill Batmans parents
						sys.exit(0)										# Take Martha's pearls
		
					# Otherwise return to standbye mode
					else:
						quit_conf = 0									# clear value
						confirm = 0										# clear value
						quit_flg = 0									# set flag
						store_flg = 0									# confirm off
					
			#################
			## ACTIVE MODE ##
			#################
			else:														# if switch HIGH - ON
				# Running entire motion detection system
				LEDS.Blink_Cyan1()					
					
	# Ctrl+C will exit the program correctly
	except KeyboardInterrupt:
		print("\r\nEXIT PROGRAM!!")										# Pistol whip Thomas Wayne
		GPIO.cleanup()													# Kill Batmans parents
		sys.exit(0)														# Take Martha's pearls

if __name__ == "__main__":	main()
