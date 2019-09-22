"""
Records 10sec audio .wav file from SAMSON USB microphone
------------------------------------------------------------
With RATE = 44100 -> IOError: [Errno -9981] Input overflowed
Changed to 48000 to solve
"""
import pyaudio
import wave

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
#RATE = 44100			# default input
RATE = 48000			# Samson microphone
DEVICE = 3				# Found with "Device1/2.py"
RECORD_SECONDS = 5         # 
WAVE_OUTPUT_FILENAME = "AUDIO.wav"

p = pyaudio.PyAudio()	# call the module
frames = []             # defined globally for both functions -> pass?

# Record data from default input device
def getAudio():
    stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input_device_index = DEVICE,
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

print"START!"
getAudio()
makeFile()
