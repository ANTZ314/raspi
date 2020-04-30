"""
Raspberry Pi time lapse (60 pics in 1 hour)
From:
http://www.makeuseof.com/tag/raspberry-pi-camera-module/

# Check ReadMe
"""
import time
import picamera

# 1 Day
VIDEO_DAYS = 1
# 1 frame per minute
FRAMES_PER_HOUR = 60
# 24 fps?
FRAMES = FRAMES_PER_HOUR * 3 * VIDEO_DAYS

def capture_frame(frame):
    with picamera.PiCamera() as cam:
        time.sleep(2)
        cam.capture('/home/pi/Pictures/t_lapse/frame%03d.jpg' % frame)

# Capture the images
for frame in range(FRAMES):
    # Note the time before the capture
    start = time.time()
    capture_frame(frame)

    # Wait for the next capture. Note that we take into
    # account the length of time it took to capture the
    # image when calculating the delay
    time.sleep( int(60 * 60 / FRAMES_PER_HOUR) - (time.time() - start) )
