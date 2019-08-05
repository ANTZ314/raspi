# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 10:09:28 2017
@author: antz
Description: - Check and auto-select audio input device
             - Initialise with this device
             - Wait for (RMS > Threshold) as trigger
             - Trigger records until 'silence time-out' to stop
Language:    - Python 3.5   [2.7 Failed]
"""

import pyaudio
import wave
import sys
#import math
#import struct

FORMAT = pyaudio.paInt16                # Default unchanged
Threshold = 50                          # Energy threshold upper from 30 dB
CHUNK = 4096                            # Audio chunk size 2**12 (default 1024)
CHANNELS = 2                            # will change according to audio device
RATE = 48000                            # Samson sample rate
DEVICE = 4                              # Will change if Audio device is found

#Threshold = 5                           # Energy threshold upper from 30 dB
#CHUNK = 1024                            # Audio chunk size 2**12 (default 1024)
#CHANNELS = 1                            # default
#RATE = 44100                            # default

WAVE_OUTPUT_FILENAME1 = "Ex4.wav"       # Storage file name 1
SHORT_NORMALIZE = (1.0/32768.0)         # What is this for?
swidth = 2                              # 
Max_Seconds = 10                        # Time-out length
Min_Seconds = 2                         # Number of seconds to prepend
RECORD_SECONDS = 5                      # increase?
TimeoutSignal=((RATE / CHUNK * Max_Seconds) + 2) 
TimeoutShort = (RATE / CHUNK * Min_Seconds)
silence = True                          # continuous loop waiting for trigger
Time=0                                  # Time out init
all =[]                                 # 

p = pyaudio.PyAudio()                   # 
info = p.get_host_api_info_by_index(0)  # 
numdevices = info.get('deviceCount')    # 
frames = []                             # defined globally for both functions -> pass?
buff = []                               # prepended buffer

stream = p.open(format = FORMAT,
                channels = CHANNELS,
                rate = RATE,
                input_device_index = DEVICE,
                input = True,
                output = True,
                frames_per_buffer = CHUNK)

def find_device():
        Found = 0                           # Device found? (1 = Yes / 0 = No)
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
            print ('Selected device is: {0}'.format(devinfo.get('name')))
            try:
                if p.is_format_supported(RATE,                                      # Sample rate
                                        input_device=devinfo["index"],              # Which device to select
                                        input_channels=devinfo['maxInputChannels'], # Number of channels
                                        input_format=FORMAT):                       # Must specify: Default
                                        #output_format=FORMAT):                     # Uses default
                                             print ('\nSupported Device -{0}- has -{1}- Channels\n'.format(str(devinfo["index"]),str(devinfo['maxInputChannels'])))
                #print ('\nSupported Device -{0}- has -{1}- Channels\n'.format(str(devinfo["index"]),str(devinfo['maxInputChannels'])))
            except ValueError:
                    print("\n16 bit Format is NOT supported!?!")
                    
        else:
            print ("\nNo Audio device found... Go with default input")
            devinfo = p.get_device_info_by_index(0)
            #sys.exit()
        return devinfo      # return all of the Audio Devices specifications

def GetStream(CHUNK):
    return stream.read(CHUNK)

def WriteSpeech(WriteData):
    wf = wave.open(WAVE_OUTPUT_FILENAME1, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

def KeepRecord(TimeoutSignal, LastBlock):
    global frames
    for i in range(0, int(TimeoutSignal)):
        data = stream.read(CHUNK)
        frames.append(data)
    
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    try:
        frames = buff + frames                              # Prepend the 2sec data to main 10sec data
    except Exception as e:
        print "Error: ", e
    
    WriteSpeech(data)                                       # Create the .wav file with the current audio stream
    print ("Write to File: {0}".format(WAVE_OUTPUT_FILENAME1))
    
    ## REPEAT ##
    #silence = True
    #Time=0
    #listen(silence,Time)
    
    ## END HERE!! ##
    print("END HERE!!")
    sys.exit()
    
def getBuff(TimeoutSignal, LastBlock, trigger):
    for i in range(0, int(TimeoutSignal)):
        data = stream.read(CHUNK)
        buff.append(data)
    trigger += 1                                            # start actual recording
    return trigger
    
def listen(silence,Time):
    counter = 0                                             # generic counter to display RMS
    trig = 0
    
    while silence:
        try:
            input = GetStream(CHUNK)                        # audio input datablock
        except:
            continue
        #rms_value = rms(input)                             # 
        #print (".", end=' ')                               # print same line {python2.x - item = "." print(item,)}
        print ".",                                          # python2 version
        
        LastBlock = input                               # Get audio data block
        ## Audio Trigger ##
        if trig == 4:
            trig = 0                                        # clear counter
            silence = False                                 # stop looping
            print "Recording..."
            KeepRecord(TimeoutSignal, LastBlock)            # keep the input data as .wav file
        ## Data to prepend before trigger data ##
        else:
            print "Listening..."
            trig = getBuff(TimeoutSignal, LastBlock, trig)       
    
        Time = Time + 1                                     # Timeout counter
        ## Time-out recording ##
        if (Time > TimeoutSignal):
            print(counter)
            print ("Time Out: No Speech Detected")
            sys.exit()
    

if __name__ == "__main__":
    devinfo = find_device()                                 # Get the details of the audio device	
    listen(silence,Time)                                    # pass found audio device details
    print("Complete...")
