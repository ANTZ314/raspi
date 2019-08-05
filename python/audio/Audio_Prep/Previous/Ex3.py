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

FORMAT = pyaudio.paInt16                # Default unchanged
Threshold = 5                           # Energy threshold upper from 30 dB
CHUNK = 4096                            # Audio chunk size 2**12 (default 1024)
CHANNELS = 2                            # will change according to audio device
RATE = 48000                            # Samson sample rate
DEVICE = 4                              # Will change if Audio device is found

#Threshold = 5                           # Energy threshold upper from 30 dB
#CHUNK = 1024                            # Audio chunk size 2**12 (default 1024)
#CHANNELS = 1                            # default
#RATE = 44100                            # default

WAVE_OUTPUT_FILENAME1 = "Ex3.wav"       # Storage file name 1
SHORT_NORMALIZE = (1.0/32768.0)         # What is this for?
swidth = 2                              # 
Max_Seconds = 10                        # Time-out length
Min_Seconds = 2                         # Prepended data
RECORD_SECONDS = 5                      # increase?
TimeoutSignal=((RATE / CHUNK * Max_Seconds) + 2)
TimeoutShort = (RATE / CHUNK * Min_Seconds)
silence = True                          # continuous loop waiting for trigger
Time=0                                  # Time out init
all =[]                                 # 

p = pyaudio.PyAudio()                   # Create PyAudio object
info = p.get_host_api_info_by_index(0)  # For finding Audio device
numdevices = info.get('deviceCount')    # For finding Audio device
frames = []                             # defined globally for both functions -> pass?
buff = []                               # continuously over-write with input data
finish = False                          # temporary ender
 
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
            print ('\nSelected device is: {0}'.format(devinfo.get('name')))
                                
        else:
            print ("\nNo Audio device found... Go with default input")
            devinfo = p.get_device_info_by_index(0)
            #sys.exit()
        return devinfo      # return all of the Audio Devices specifications
        #return DEVICE

def GetStream(CHUNK):
    return stream.read(CHUNK)

def WriteSpeech(WriteData):    
    wf = wave.open(WAVE_OUTPUT_FILENAME1, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

def getBuff(TimeoutShort, LastBlock, trigger):
    for i in range(0, int(TimeoutShort)):                       # about 4sec
        data = stream.read(CHUNK)
        buff.append(data)
    trigger += 1                                                # start actual recording
    return trigger

def KeepRecord(TimeoutSignal, LastBlock):
    global frames                                               # avoid pre-accessing error
    for i in range(0, int(TimeoutSignal)):                      # 10sec
        data = stream.read(CHUNK)                               # stream audio data
        frames.append(data)                                     # gather streamed data chunks
    
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    try:
        frames = buff + frames                                  # append the data
    except Exception as e:
        print "Error: ", e
    
    WriteSpeech(data)                                           # Create the .wav file with the current audio stream
    print "Write to File: {0}".format(WAVE_OUTPUT_FILENAME1)
    
    finish = True
    return finish

def main():
    trig = 0
    finish = False      # remove
    
    devinfo = find_device()
    print ('Device No. -{0}- has -{1}- Channels\n'.format(str(devinfo["index"]),str(devinfo['maxInputChannels'])))
    
    while silence:
        try:
            input = GetStream(CHUNK)                            # audio input datablock
        except:
            continue
        
        LastBlock = input                                       # needed for 'getBuff' & 'KeepRecord'
        if(trig == 2):                                          # Get audio data block (need 2nd buffer)
            print "Recording..."
            finish = KeepRecord(TimeoutSignal, LastBlock)       # keep the input data as .wav file
        else:
            print "Listening..."
            trig = getBuff(TimeoutShort, LastBlock, trig)       # continuously get 4sec chunk over-writing
        
        ## Time-out recording ##
        if finish:
            print "Recorded & Exited"
            sys.exit()                                          # end and exit
        
if __name__ == "__main__": main()
