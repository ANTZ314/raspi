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

def main():
    # Instantiate the class
    Face = FaceCnt.faceCntClass()       # Create object to access 'FaceCnt' Class
    Face.message("Images...")			# Pass text message to the class
    
    FaceNum = Face.FaceCounter()        # Call the main Face Finder
    Face.UseFace(FaceNum)  				# Use the number of faces  
    print("Complete...")
    
if __name__ == "__main__": main()
