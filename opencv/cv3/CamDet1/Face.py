# -*- coding: utf-8 -*-
"""
Description:
Main file for main facial detection
Opens default webcam and detects faces
'q' to exit

Run the program like this:
$ python Face.py
"""
import faceDet1 as faceDet

Image_No = 0							# number of images stored
FaceNum = 0								# number of faces
cnt = 0									# generic counter 

def main():
	Face = faceDet.DetectClass()
	Face.message("Camera...")
		
	Face.detect()
			
	print("Complete...")
    
if __name__ == "__main__": main()
