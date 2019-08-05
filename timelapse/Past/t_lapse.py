# -*- coding: utf-8 -*-
"""
Raspberry Pi time lapse (60 pics in 1 hour)
From:
http://www.makeuseof.com/tag/raspberry-pi-camera-module/

* Frist install:
$ sudo apt-get install libav-tools

* Then run this python script (60min capture)
	-> >Error: timed out waiting for capture to end?

* Then To view the images as a film, compile the images:
$ ffmpeg -y -f image2 -i /home/pi/Pictures/timelapse/frame%03d.jpg -r 24 -vcodec libx264 -profile high -preset slow /home/pi/Desktop/timelapse.mp4

-> ffmpeg changed so create an alias to the new one:
-> in "~/.bashrc" add this line:
-> alias ffmpeg=avconv

Play in OMX:
omxplayer timelapse.mp4
"""
import time
import picamera

path3 = "/home/pi/Pictures/t_lapse/frame%03d.jpg"	

VIDEO_DAYS = 1
FRAMES_PER_HOUR = 60
FRAMES = FRAMES_PER_HOUR * 24 * VIDEO_DAYS

def capture_frame(frame):
    with picamera.PiCamera() as cam:
        time.sleep(2)
        #cam.capture('/home/pi/Pictures/t_lapse/frame%03d.jpg' % frame)
        cam.capture(str(path3) % frame, use_video_port=True)	
		
def main():
	print "LET'S BEGIN!!"
	try:
		# Capture the images
		for frame in range(FRAMES):
			# Note the time before the capture
			start = time.time()
			capture_frame(frame)

			# Wait for the next capture. Note that we take into
			# account the length of time it took to capture the
			# image when calculating the delay
			time.sleep( int(60 * 60 / FRAMES_PER_HOUR) - (time.time() - start) )
	# Ctrl+C will exit the program correctly
	except KeyboardInterrupt:
		print("\r\nEXIT PROGRAM!!")										# Pistol whip Thomas Wayne
		#GPIO.cleanup()													# Kill Batmans parents
		sys.exit(0)	
		
if __name__ == "__main__":	main()
