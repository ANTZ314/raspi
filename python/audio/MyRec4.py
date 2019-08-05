"""
Record .wav file from 3.5mm jack to USB adapter
-----------------------------------------------
-> Only works with Python 3.x, though should work on both
"""
import pyaudio
import wave


FORMAT = pyaudio.paInt16
CHUNK = 1024
CHANNELS = 1			    # Kibult
RATE = 44100			    # Samson microphone
DEVICE = 0			    # Found with "Device1/2.py"

#CHUNK = 4096
#CHANNELS = 2			    # Kibult
#RATE = 48000			    # Samson microphone
#DEVICE = 4				    # Found with "Device1/2.py"

RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "AUDIO4.wav"

p = pyaudio.PyAudio()	   # call the module
frames = []             # defined globally for both functions -> pass?

# Record data from default input device
def getAudio():
    print("START!")
    stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
#                input_device_index = DEVICE,
                input=True,
                frames_per_buffer=CHUNK)
                
    print("* recording")
    
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
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

if __name__ == "__main__":
    getAudio()
    makeFile()
