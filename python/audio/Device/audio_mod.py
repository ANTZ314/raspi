# -*- coding: utf-8 -*-
"""
Created on Mon May 15 14:29:28 2017
@author: antz

A\Description: Test PyAudio Module

Error in Python 2.7.13 ? ?
Runs  in Python 3.4.xx 

Lines [57-61] used to compile in both 2.7 & 3.4 ? ? ? 
Error:
p.is_format_supported -> Error on "input_format=FORMAT" ???

"""

import pyaudio
import sys

FORMAT = pyaudio.paInt16                # Default unchanged
Threshold = 5                           # Energy threshold upper from 30 dB
CHUNK = 4096                            # Audio chunk size 2**12 (default 1024)
CHANNELS = 2                            # will change according to audio device
RATE = 48000                            # Samson sample rate
DEVICE = 4                              # Will change if Audio device is found

p = pyaudio.PyAudio()                   # 
info = p.get_host_api_info_by_index(0)  # 
numdevices = info.get('deviceCount')    # 

max_apis = p.get_host_api_count()
max_devs = p.get_device_count()

stream = p.open(format = FORMAT,
                channels = CHANNELS,
                rate = RATE,
                input_device_index = DEVICE,
                input = True,
                output = True,
                frames_per_buffer = CHUNK)
                

def find_device():    
        print ("=" * 90)
        print ("PortAudio System Info:")
        print ("=" * 90)
        print ("Version: %d" % pyaudio.get_portaudio_version())
        print ("Version Text: %s" % pyaudio.get_portaudio_version_text())
        print ("Number of Host APIs: %d" % max_apis)
        print ("Number of Devices  : %d\n" % max_devs)    
    
        Found = 0                       # Device found? (1 = Yes / 0 = No)
        #for each audio device, determine if is an input or an output and add it to the appropriate list and dictionary
        for i in range (0,numdevices):
                if p.get_device_info_by_host_api_device_index(0,i).get('maxInputChannels')>0:
                        print (" Input Device id {0} - {1}".format(i, p.get_device_info_by_host_api_device_index(0,i).get('name')))
                        if 'Audio' in str(p.get_device_info_by_host_api_device_index(0,i).get('name')):                            
                            Found = 1
                            DEVICE = i
        
                if p.get_device_info_by_host_api_device_index(0,i).get('maxOutputChannels')>0:
                        print ("Output Device id {0} - {1}".format(i, p.get_device_info_by_host_api_device_index(0,i).get('name')))
        
        if Found == 1:
            # Manually using the device index of Samson Microphone
            devinfo = p.get_device_info_by_index(DEVICE)
            print ('\nSelected device is: {0}\n'.format(devinfo.get('name')))
            
            try:
                if p.is_format_supported(RATE,                                      # Sample rate
                                        input_device=devinfo["index"],              # Which device to select
                                        input_channels=devinfo['maxInputChannels'], # Number of channels
                                        input_format=FORMAT):                       # Default
                                        #output_format=FORMAT):
                                             print ('\nSupported Device -{0}- has -{1}- Channels\n'.format(str(devinfo["index"]),str(devinfo['maxInputChannels'])))
                #print ('\nSupported Device -{0}- has -{1}- Channels\n'.format(str(devinfo["index"]),str(devinfo['maxInputChannels'])))
            except ValueError:
                    print("\n16 bit Format is NOT supported!?!")
                
        else:
            print ("\nNo Audio device found... Exit for now")
            sys.exit()
        return devinfo      # return all of the Audio Devices specifications
        
if __name__ == "__main__":
    devinfo = find_device()     # Get the details of the audio device
    print("Finished...")