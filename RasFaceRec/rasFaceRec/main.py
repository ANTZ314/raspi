# -*- coding: utf-8 -*-
"""
Description:
Main class calling data capture class and facial recognition class
Also uses classification results to decide reaction and play video accordingly

Dependencies:
imutils, face_recognition, dlib, cv2

Usage:
python3 main.py
"""
import dataset as Dataset
import recog as Recog
import ledClass as leds
import os, subprocess

dog = "/home/pi/Documents/rasFaceRec/dataset/dog.gif"
tit = "/home/pi/Documents/rasFaceRec/dataset/tit.gif"

def main():
    #Here we show how to instantiate your class
    Data = Dataset.DatasetClass()               # Create object to access 'Face Capture' Class
    Face = Recog.RecogClass()				    # Create object to access 'Recognition Testing' Class
    Leds = leds.LEDClass()                      # Create object to access 'LED Control' Class
    
    key = input("Capture new image: y/n - ")
    # User chose to capture new image:
    if key == 'y':
        print("Then press k to capture & q to exit")
        Leds.Quick_Green1()
        Data.getPerson()                   		# Manual capture of person
    # User chose not to capture new image:
    elif key == 'n':
        print("selected not to capture... what will it test?")
        Leds.Quick_Red1()
        
    while(1):
        key = input("Press: `a` to test, `q` to quit: ")
        
        if key == 'a':
            print("Find the face!!")
            person = Face.recPerson()
            
            # if no name was prominent
            if person == "Unknown":
                print("ACCESS DENIED MOFO!!!")
                #os.system('xdg-open dataset/dog.gif')
                #subprocess.call(['vlc',dog,'--play-and-exit'])      # ESC to exit vlc
                Leds.Blink_Green1()
                Leds.Blink_Green1()
                Leds.Blink_Green1()
            else:
                print("YOU MAY ENTER!!!")
                #os.system('xdg-open dataset/tit.gif')
                subprocess.call(['vlc',tit,'--play-and-exit'])      # ESC to exit vlc
                Leds.Blink_Red1()
                Leds.Blink_Red1()
                Leds.Blink_Red1()
                
            print("complete!")
            
        elif key == 'q':
            break
            
        else:
            print("Invalid Selection Retard!!")
            
    print("EXITING...")

   
if __name__ == "__main__": main()
