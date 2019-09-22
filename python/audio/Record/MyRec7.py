# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 12:09:28 2017
@author: antz
Description: - Check and auto-select audio input device
             - Initialise with default device (not found device)
             - Wait for RMS > Threshold as trigger
             - Trigger records until 'silence time-out' to stop
"""

import pyaudio
import math
import struct
import wave
import sys

#Assuming Energy threshold upper from 30 dB
Threshold = 2                          # was 30

FORMAT = pyaudio.paInt16                # Default unchanged
#CHUNK = 4096                            # Audio chunk size 2**12 (default 1024)
#CHANNELS = 2                            # will change according to audio device
#RATE = 48000                            # Samson sample rate
DEVICE = 0                              # Found with "Device1/2.py"
CHUNK = 1024                            # Audio chunk size 2**12 (default 1024)
CHANNELS = 1                            # default
RATE = 44100                            # default
RECORD_SECONDS = 5                      # increase?
WAVE_OUTPUT_FILENAME = "AUDIO7.wav"     # Storage file name

SHORT_NORMALIZE = (1.0/32768.0)         # What is this for?
swidth = 2                              # 
Max_Seconds = 10                        # Time-out length
TimeoutSignal=((RATE / CHUNK * Max_Seconds) + 2)    # 2.46875 ?
silence = True                          #
Time=0                                  #
all =[]                                 #

p = pyaudio.PyAudio()                   #
info = p.get_host_api_info_by_index(0)  #
numdevices = info.get('deviceCount')    #
frames = []                             # defined globally for both functions -> pass?

stream = p.open(format = FORMAT,
                channels = CHANNELS,
                rate = RATE,
                #input_device_index = DEVICE,
                input = True,
                output = True,
                frames_per_buffer = CHUNK)

def find_device():
    Okay = 0        # Device found? (1 = Yes / 0 = No)
    #for each audio device, determine if is an input or an output and add it to the appropriate list and dictionary
    for i in range (0,numdevices):
            if p.get_device_info_by_host_api_device_index(0,i).get('maxInputChannels')>0:
                    print (" Input Device id {0} - {1}".format(i, p.get_device_info_by_host_api_device_index(0,i).get('name')))
                    if 'Audio' in str(p.get_device_info_by_host_api_device_index(0,i).get('name')):
                        Okay = 1
                        DEVICE = i
    
            if p.get_device_info_by_host_api_device_index(0,i).get('maxOutputChannels')>0:
                    print ("Output Device id {0} - {1}".format(i, p.get_device_info_by_host_api_device_index(0,i).get('name')))
                    #print ("Output Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0,i).get('name'))
    
    if Okay == 1:
        devinfo = p.get_device_info_by_index(DEVICE)
        print ('Selected device is: {0}'.format(devinfo.get('name')))
        
        if p.is_format_supported(RATE,
                             input_device=devinfo["index"],
                             input_channels=devinfo['maxInputChannels'],
                             input_format=pyaudio.paInt16):
                                 print ('\nSupported Device Info:\nDevice Number: {0}\nWith Channels: {1}'.format(str(devinfo["index"]),str(devinfo['maxInputChannels'])))

    else:
        print "No Audio device found... Exit for now"
        sys.exit()

    #print("\nTerminating...")
    #p.terminate()

def GetStream(CHUNK):
    return stream.read(CHUNK)

def rms(frame):
        count = len(frame)/swidth
        format = "%dh"%(count)
        shorts = struct.unpack( format, frame )

        sum_squares = 0.0
        for sample in shorts:
            n = sample * SHORT_NORMALIZE
            sum_squares += n*n
        rms = math.pow(sum_squares/count,0.5)       # had a ';' ?

        return rms * 1000

def WriteSpeech(WriteData):
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(WriteData)
    wf.close()

def KeepRecord(TimeoutSignal, LastBlock):

    all.append(LastBlock)
    for i in range(0, TimeoutSignal):
        try:
            data = GetStream(CHUNK)
        except:
            continue
        #I chage here (new Ident)
        all.append(data)

    print "End record after timeout"
    data = ''.join(all)
    print "Write to File: {0}".format(WAVE_OUTPUT_FILENAME)
    WriteSpeech(data)
    #silence = True
    #Time=0
    #listen(silence,Time)
    print"END HERE!!"
    sys.exit()

def listen(silence,Time):
    count = 0
    print "waiting for Speech"
    while silence:

        try:
            input = GetStream(CHUNK)

        except:
            continue

        rms_value = rms(input)
        count += 1

        if count == 80:
            print("{0}".format(rms_value))
            count = 0               # restart counter

        if (rms_value > Threshold):
            silence=False
            LastBlock=input
            print "I'm Recording...."
            KeepRecord(TimeoutSignal, LastBlock)

        Time = Time + 1

        if (Time > TimeoutSignal):
            print "Time Out: No Speech Detected"
            sys.exit()

if __name__ == "__main__":
    devinfo = find_device()     # Get the details of the audio device
    print "Begin Process..."	
    listen(silence,Time)        # pass found audio device details
    #getAudio(devinfo)
    #makeFile()
    print("Complete...")