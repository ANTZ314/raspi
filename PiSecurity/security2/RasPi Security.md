
### Security Camera:
* master.py - runs subprocess to open security folder and run the *main.py* file
* main.py - calls all subprocesses including LED and buttons, motion detection camera process, storage to USB (then wipe) and the shutdown process.

*NOTE - after images copied to USB need to go back to zero on the image naming* 

### Run at boot:

	sudo crontab -e

Add the following to run (# to comment out):

	python master.py

--------------------------------
[Security System](https://www.pyimagesearch.com/2015/06/01/home-surveillance-and-motion-detection-with-the-raspberry-pi-python-and-opencv/)

[Motion Detection:](https://www.pyimagesearch.com/2015/05/25/basic-motion-detection-and-tracking-with-python-and-opencv/)

[Other versions:](https://www.bouvet.no/bouvet-deler/utbrudd/building-a-motion-activated-security-camera-with-the-raspberry-pi-zero
https://medium.com/@Cvrsor/how-to-make-a-diy-home-alarm-system-with-a-raspberry-pi-and-a-webcam-2d5a2d61da3d)