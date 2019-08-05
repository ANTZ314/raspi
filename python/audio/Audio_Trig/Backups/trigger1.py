"""
Description: 
"""

import pyaudio
import math
import struct
import wave
import sys

#Assuming Energy threshold upper than 30 dB
Threshold = 5                      # was 30

SHORT_NORMALIZE = (1.0/32768.0)		# for?
FORMAT = pyaudio.paInt16

#CHUNK = 4096                        # default 1024
#CHANNELS = 2                        # default 1
#RATE = 48000					# default 44100
#DEVICE = 4                          # Default to select a new input

CHUNK = 1024                         # default
CHANNELS = 1                         # default
RATE = 44100                         # default
swidth = 2
Max_Seconds = 10
TimeoutSignal=((RATE / CHUNK * Max_Seconds) + 2)    # 2.46875 ?
silence = True
FileNameTmp = 'Audio.wav'
Time=0
all =[]

p = pyaudio.PyAudio()
	
stream = p.open(format = FORMAT,
                channels = CHANNELS,
                rate = RATE,
                #input_device_index = DEVICE,
                input = True,
                output = True,
                frames_per_buffer = CHUNK)

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
        rms = math.pow(sum_squares/count,0.5);

        return rms * 1000

def WriteSpeech(WriteData):
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf = wave.open(FileNameTmp, 'wb')
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
    print "Write to File: {0}".format(FileNameTmp)
    WriteSpeech(data)
    silence = True
    Time=0
    print"END HERE!!"
    sys.exit()
    #listen(silence,Time)

def listen(silence,Time):
    count = 0                       # generic counter
    print "Waiting for Speech..."
    while silence:

        try:
            input = GetStream(CHUNK)

        except:
            continue

        rms_value = rms(input)
        count += 1
        
        if count == 50:
            print("{0}".format(rms_value))     
            count = 0               # restart counter

        if (rms_value > Threshold):
            silence=False
            LastBlock=input
            print "I'm Recording...."
            KeepRecord(TimeoutSignal, LastBlock)

        Time = Time + 1

        if (Time > TimeoutSignal):
            print "Time-Out: No Speech Detected!"
            sys.exit()

def main():
    #print "Begin Process..."	
    listen(silence,Time)
    print "Finished..?"

if __name__ == "__main__":main()
