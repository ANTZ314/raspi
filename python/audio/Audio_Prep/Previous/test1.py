# -*- coding: utf-8 -*-
"""
Checking input devices for the SAMSON then use that device[index] for recording function
"""
import pyaudio
import wave
#import math
#import struct
import sys

FORMAT = pyaudio.paInt16                # Default unchanged
Threshold = 50                          # Energy threshold upper from 30 dB
CHUNK = 4096                            # Audio chunk size 2**12 (default 1024)
CHANNELS = 1                            # will change according to audio device
RATE = 48000                            # Samson sample rate
DEVICE = 4                              # Will change if Audio device is found
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "test.wav"

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

# Record data from default input device
def getAudio():
    stream = p.open(format=FORMAT,
                channels=CHANNELS,              # devinfo['maxInputChannels'],
                rate=RATE,
                input_device_index = DEVICE,    # devinfo["index"],
                input=True,
                frames_per_buffer=CHUNK)
                
    print("* start recording")
    
    #frames = []                # now global

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    
    print("* done recording")
    
    stream.stop_stream()
    stream.close()
    p.terminate()

# Create the .wav file from previous recorded data
def makeFile():
    print ("* creating file named: {0}".format(WAVE_OUTPUT_FILENAME))
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

if __name__ == "__main__":
    find_device()
    getAudio()
    makeFile()
    print("Complete...")
    
