# -*- coding: utf-8 -*-
"""
Description:
General Python File Template

USAGE:
python name.py
"""
######################
## IMPORT LIBRARIES ##
######################
import 


#####################
##  MAIN FUNCTION  ##
#####################
def main():	
	try:
		try:
			
			
			print("DONE!!")					# Guess what this does??
			sys.exit(0)						# exit properly
			
		# Ctrl+C will exit the program correctly
		except KeyboardInterrupt:
			print("Keyboard Interupt")
			#GPIO.cleanup()
			sys.exit(0)
		
	# Any Main Errors saved to log.txt file:
	except Exception:
		print("Exception reached - Check Log.txt File")
		log = open("log.txt", 'w')
		traceback.print_exc(file=log)
		sys.exit(0)


if __name__ == "__main__":	main()
