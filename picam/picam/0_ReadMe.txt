-------------
CAMERA NOTES:
-------------
raspistill -vf -hf -o
	[-vf -> vertical flip]
	[-hf -> horizontal flip]
	
For a list of arguments, run:
$ raspistill
OR
$ raspistill 2>&1 | less
'q' to exit

=====================================
To convert to playable MP4:
=====================================
sudo apt iupdate
sudo apt install -y gpac

MP4Box-fps 30 -add myvid.h264 myvid.mp4

=====================================
	    PYTHON
=====================================
To rotate the image:
>> camera.rotation = 90

=====================================
	VIDEO PLAYBACK
=====================================
$ omxplayer video.h264

