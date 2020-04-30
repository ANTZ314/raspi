"""
To Run:
python /home/pi/Pictures/timelapse/PyPiCam.py
"""
import picamera

# create an instance
camera = picamera.PiCamera()

# To flip views
#camera.hflip = True
#camera.vflip = True

#crop camera
camera.crop = (0.0, 0.0, 1.0, 1.0)

#view overlay
camera.start_preview()
# Stop overlay
camera.stop_preview()

# Take a picture
camera.capture('/home/pi/Pictures/timelapse/image0.jpg')
