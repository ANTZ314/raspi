# -*- coding: utf-8 -*-
"""
Description:
Main class calling data capture class and facial recognition class
Also uses classification results to decide reaction and play video accordingly

Usage:
python3 main.py
"""
import dataset as Dataset
import recog as Recog
import os, subprocess

dog = "/home/antz/GIT31/OpenCV/FaceRec/faceReact/dataset/dog.gif"
tit = "/home/antz/GIT31/OpenCV/FaceRec/faceReact/dataset/tit.gif"

def main():
    #Here we show how to instantiate your class
    Data = Dataset.DatasetClass()           # Create object to access 'Face Capture' Class
    Face = Recog.RecogClass()				# Create object to access 'Recognition Testing' Class
    
    key = input("Capture new image: y/n - ")
    if key == 'y':
        print("Then press k to capture & q to exit")
        Data.getPerson()                   		# allow for manual capture of person

    while(1):
    	key = input("Press: `a` to test, `q` to quit: ")

    	if key == 'a':
    		print("Find the face!!")
    		person = Face.recPerson()

    		# if no name was prominent
    		if person == "Unknown":
    			print("ACCESS DENIED MOFO!!!")
    			#os.system('xdg-open dataset/dog.gif')
                subprocess.call(['vlc',dog,'--play-and-exit'])      # ESC to exit vlc
    		else:
    			print("YOU MAY ENTER!!!")
    			#os.system('xdg-open dataset/tit.gif')
                subprocess.call(['vlc',tit,'--play-and-exit'])      # ESC to exit vlc

            print("complete!")

    	elif key == 'q':
    		break

    	else:
    		print("Invalid Selection Retard!!")

    print("EXITING...")
    
if __name__ == "__main__": main()