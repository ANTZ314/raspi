# -*- coding: utf-8 -*-
"""
Description:
Main class calling data capture class and facial recognition class
Also uses classification results to decide reaction and play video accordingly

Usage:
python3 main.py
"""
#import dataset as Dataset
#import recog as Recog
import os, subprocess

dog = "/home/antz/GIT31/OpenCV/FaceRec/faceReact/dataset/dog.gif"
tit = "/home/antz/GIT31/OpenCV/FaceRec/faceReact/dataset/tit.gif"

def main():
    key = input("Capture new image: y/n - ")
    if key == 'y':
        print("Then press k to capture & q to exit")
        while(1):
            key = input("Press: `a` to test, `q` to quit: ")

            if key == 'a':
                print("ACCESS DENIED MOFO!!!")
            elif key == 'q':
                break
            else:
                print("Invalid Selection Retard!!")

    elif key == 'n':
        print("Exit Early!")

    print("EXITING...")
    
if __name__ == "__main__": main()