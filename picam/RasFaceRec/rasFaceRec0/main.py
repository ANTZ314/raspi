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

dog = "/home/antz/git314/raspi/picam/RasFaceRec/rasFaceRec0/dataset/dog.gif"
tit = "/home/antz/git314/raspi/picam/RasFaceRec/rasFaceRec0/dataset/tit.gif"
lok = "/home/antz/git314/raspi/picam/RasFaceRec/rasFaceRec0/dataset/lock.mp4"

def main():
    #Here we show how to instantiate your class
    Data = Dataset.DatasetClass()                       # Create object to access 'Face Capture' Class
    Face = Recog.RecogClass()				            # Create object to access 'Recognition Testing' Class
    
    while(1):
        key = input("Capture new image: y/n - ")
        if key == 'y':
            print("Then press k to capture & q to exit")
            Data.getPerson()                   	            # allow for manual capture of person

            while(1):
                key = input("Press: `a` to test, `q` to quit: ")

                if key == 'a':
                    print("Find the face!!")
                    person = Face.recPerson()               # Identification process

                    # if no name was prominent
                    if person == "Unknown":
                        print("ACCESS DENIED MOFO!!!")
                        os.system('xdg-open dataset/dog.gif')                # Ubuntu
                        #subprocess.call(['vlc',dog,'--play-and-exit'])      # RasPi
                    else:
                        print("YOU MAY ENTER!!!")
                        #os.system('xdg-open dataset/lock.gif')              # Ubuntu
                        #os.system('xdg-open dataset/lock.mp4')               # Ubuntu
                        #subprocess.call(['vlc',tit,'--play-and-exit'])      # RasPi??
                        subprocess.call(['vlc',lok,'--play-and-exit'])      # RasPi??

                    print("complete!")

                elif key == 'q':
                    break

                else:
                    print("Invalid Selection, Retard!!")
        else:
            print("Going no further...")
            break

    print("EXITING...")
    
if __name__ == "__main__": main()