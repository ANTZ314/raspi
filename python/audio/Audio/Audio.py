# -*- coding: utf-8 -*-
"""
Created on Feb 3rd 10:08:20 2017
@author: Antony Smith
@description: Class of Audio Operators
"""
import AudioClass as Audio

def main():
    #Here we show how to instantiate your class
    Aud = Audio.AudioClass()            # Create object to access 'Audioclass' Class
    #Aud.message("...and so it begins") # Pass test message to the class
    
    Aud.find_device()                   # Check all input & output devices for audio input
    Aud.getAudio()                      # Setup PyAudio using selected device and record
    Aud.makeFile()                      # Store the recorded audio clip to .wav file
    print("Complete...")
    
if __name__ == "__main__": main()