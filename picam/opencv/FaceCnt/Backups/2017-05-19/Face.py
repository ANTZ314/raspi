# -*- coding: utf-8 -*-
"""
Created on: 	[2017-05-09]
@author: 		Antony Smith
@description: 	Opens image at predefined location counts faces
				If file doesn't exist, creates file and appends
				image directory/name.jpg and number of faces counted

Run:			python Face.py
"""
import faceCnt2 as FaceCnt

Image_No = 0							# number of images stored
FaceNum = 0								# number of faces
cnt = 0									# generic counter 

def main():
	Face = FaceCnt.faceCntClass()
	Face.message("Images...")
	
	Image_No = Face.No_images()
	
	for count in range(0, Image_No): 
		FaceNum = Face.FaceCounter() 
		Face.UseFace(FaceNum, count)
		
	print("Complete...")
    
if __name__ == "__main__": main()
