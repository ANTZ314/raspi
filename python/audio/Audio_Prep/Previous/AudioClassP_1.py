# -*- coding: utf-8 -*-
"""
Created on Feb 3rd 10:08:20 2017
@author: Antony Smith
@description: Class containing functions to find audio device, then initialise stream
              using that devices details, then wait for an audio trigger to start recording
              a predefined sound clip (10sec?) or stop when no audio recieved (time-out for both)
"""
import pyaudio
import math
import struct
import wave
import sys
  
class AudioClass:  
    
    FORMAT = pyaudio.paInt16                # Default unchanged
    Threshold = 3                           # Energy threshold upper from 30 dB
    CHUNK = 4096                            # Audio chunk size 2**12 (default 1024)
    CHANNELS = 2                            # Will change to device's default
    RATE = 48000                            # Samson sample rate
    DEVICE = 0				            # Found with "Device1/2.py" - Changes!
    
    RECORD_SECONDS = 5                      # Max audio record time (fails on higher?)
    WAVE_OUTPUT_FILENAME = "AUDIO_T.wav"    # Output Filename
    SHORT_NORMALIZE = (1.0/32768.0)         # What is this for?
    swidth = 2                              # 
    Max_Seconds = 10                        # Time-out length
    TimeoutSignal=((RATE / CHUNK * Max_Seconds) + 2) # 2.46875 ?
    silence = True                          # ?
    Time=0                                  # ?
    all =[]                                 # ?
    block =[]
    frames = []                             # defined globally for both functions -> pass?

    #########################
    ## Class instantiation ##
    #########################
    def __init__(self, **kwargs):
        print("Stream init!!")
        self.p = pyaudio.PyAudio()
        self.info = self.p.get_host_api_info_by_index(0)
        self.numdevices = self.info.get('deviceCount')
        self.stream = self.p.open(format = self.FORMAT,
                channels = self.CHANNELS,
                rate = self.RATE,
                input_device_index = self.DEVICE,
                input = True,
                output = True,
                frames_per_buffer = self.CHUNK)
    
    ## Can Remove - Startup message ## 
    def message(self, string):
        print("Warp Speed... {0}\n".format(str(string)))
    
    ####################################################################################
    ## Check all Input/Output devices for any 'Audio' Input Devices & get its details ##
    ####################################################################################
    def find_device(self):
        Found = 0                           # Device found? (1 = Yes / 0 = No)
        #for each audio device, determine if is an input or an output and add it to the appropriate list and dictionary
        for i in range (0,self.numdevices):
                if self.p.get_device_info_by_host_api_device_index(0,i).get('maxInputChannels')>0:
                        print (" Input Device id {0} - {1}".format(i, self.p.get_device_info_by_host_api_device_index(0,i).get('name')))
                        if 'Audio' in str(self.p.get_device_info_by_host_api_device_index(0,i).get('name')):                            
                            Found = 1
                            self.DEVICE = i
        
                if self.p.get_device_info_by_host_api_device_index(0,i).get('maxOutputChannels')>0:
                        print ("Output Device id {0} - {1}".format(i, self.p.get_device_info_by_host_api_device_index(0,i).get('name')))
        
        if Found == 1:
            # Manually using the device index of Samson Microphone
            devinfo = self.p.get_device_info_by_index(self.DEVICE)
            print ('Selected device is: {0}'.format(devinfo.get('name')))
            
            if self.p.is_format_supported(self.RATE,                            # Sample rate
                                     input_device=devinfo["index"],             # Which device to select
                                     input_channels=devinfo['maxInputChannels'],# Number of channels
                                     input_format=self.FORMAT):                 # Default
                                         print ('\nSupported Device -{0}- has -{1}- Channels\n'.format(str(devinfo["index"]),str(devinfo['maxInputChannels'])))
        else:
            print ("\nNo Audio device found... Exit for now")
            sys.exit()
        return devinfo      # return all of the Audio Devices specifications

###############################################################################

    ############################################
    ## Could move this directly into Listen() ##
    ############################################
    def GetStream(self):
        return self.stream.read(self.CHUNK)
        
    ################################################################
    ## Calculation and comparison against predefined dB Threshold ##
    ################################################################
    def rms(self, frame):
            count = len(frame)/self.swidth
            format = "%dh"%(count)
            shorts = struct.unpack( format, frame )
    
            sum_squares = 0.0
            for sample in shorts:
                # sample is a signed short in +/- 32768. 
                # normalize it to 1.0
                n = sample * self.SHORT_NORMALIZE
                sum_squares += n*n
            rms = math.pow(sum_squares/count,0.5);
    
            return rms * 1000   
            
    ################################################
    ## Write the recorded sound clip to .wav file ##
    ################################################
    def WriteSpeech(self, WriteData):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        wf = wave.open(self.WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(WriteData)
        wf.close()
    
    ##################################################
    ## Record the Audio Input until Timeout reached ##
    ##################################################
    def KeepRecord(self, TimeoutSignal, LastBlock):
        
        all.append(LastBlock)                                    # all.append(LastBlock)
        TimeoutSignal = math.floor(TimeoutSignal)                # convert float to int for range
        for i in range(0, TimeoutSignal):
            try:
                self.data = self.GetStream(self.CHUNK)
            except:
                continue
            # I change here (new Identity?)
            all.append(self.data)                                # all.append(self.data) 
    
        print ("End record after timeout")
        self.data = ''.join(all)                                 # self.data = ''.join(all)
        print ("Write to File: {0}".format(self.WAVE_OUTPUT_FILENAME))
        #self.WriteSpeech(self.data)
        
        #------------------------------#
        ## Loop continuously for Audio##
        #------------------------------#
        #silence = True
        #Time=0
        #listen(silence,Time)

        ## Temporarily End here!
        print("END HERE!!")
        sys.exit()            
    
    #######################################################
    ## Get audio input stream from selected Audio Device ##
    #######################################################
    def listen(self, silence, Time, devinfo):    
        counter = 0                                    # generic counter to display RMS
        #item = "."                                     # count indicator for RMS display
        
        while silence:
            try:
                input = self.GetStream()
            except:
                continue
            
            self.rms_value = self.rms(input)            # Get the average/normalised RMS value
            #print (".", end=' ')                        # print same line {python2.x - item = "." print(item,)}
            counter += 1                                # counter to not show RMS too often
            
            ## Continuously Print the RMS value ##
            if counter == 5:                            # after every 5 iterations
                print("{:.5f}".format(self.rms_value))     # print the current RMS value
                counter = 0                             # restart counter
            
            if (self.rms_value > self.Threshold):       # If input stream is higher than threshold
                print ("{:.5f}\nRecording...".format(self.rms_value)) # Print the input value
                silence=False                          # Exit the while loop
                LastBlock=input
                self.KeepRecord(self.TimeoutSignal, LastBlock)
                
            Time = Time + 1                             # Timeout counter
    
            if (Time > self.TimeoutSignal):             # If time counter reaches timeout value
                print ("Time Out: No Speech Detected")  # Indicate so
                sys.exit()                              # exit completely
    

