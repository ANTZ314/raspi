"""
PyAudio Example: Make a wire between input and output (i.e., record a
few samples and play them back immediately).
"""

import pyaudio

CHUNK = 1024
WIDTH = 2
CHANNELS = 2
RATE = 44100		# default input
RATE = 48000		# Samson microphone
DEVICE = 4			# Found with "Device1/2.py"
RECORD_SECONDS = 10

p = pyaudio.PyAudio()

stream = p.open(format=p.get_format_from_width(WIDTH),
                channels=CHANNELS,
                rate=RATE,
                input_device_index = DEVICE,
                input=True,
                output=True,
                frames_per_buffer=CHUNK)

print("* recording")

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    stream.write(data, CHUNK)

print("* done")

stream.stop_stream()
stream.close()

p.terminate()
