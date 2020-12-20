#RASPI VIDEO FUNCTIONS:

**Contents:**

* Concatenate multiple MP4 files into one video file
* Complile multiple images into video file (timelapse)
* Dedicated video looper - continuously loop short videos


##CONCATINATE MULTIPLE MP4 FILES:

####METHOD 1:

// First trans-code to intermediate streams:
ffmpeg -i a1.mp4 -c copy -bsf:v h264_mp4toannexb -f mpegts temp1.ts
ffmpeg -i a2.mp4 -c copy -bsf:v h264_mp4toannexb -f mpegts temp2.ts
ffmpeg -i a3.mp4 -c copy -bsf:v h264_mp4toannexb -f mpegts temp3.ts
// Then join:
ffmpeg -i "concat:temp1.ts|temp2.ts|temp3.ts" -c copy -bsf:a aac_adtstoasc output.mp4


####METHOD 2:

CREATE A TEXT FILE WITH A LIST FILES + PATHS:
```
file '/home/antz/Videos/test/a1.mp4'
file '/home/antz/Videos/test/a2.mp4'
file '/home/antz/Videos/test/a3.mp4'
```
THEN RUN THE FOLLOWING:
```
ffmpeg -f concat -safe 0 -i input.txt -c copy output.mp4
```

##COMPILE MULTIPLE IMAGES INTO VIDEO FILE:

**Note:** Images must have height/width both devisible by 2:

* -i = input files path
* -y = output file path
* framerate = defaults to 25
* -r = set frame rate


####BATCH RESIZE FILES:

* Set bash input/output file locations
* Run bash script
```
./resize.sh
```

####Compile into Video file:
```
ffmpeg -framerate 10 -i /home/antz/Pictures/pic/location/%d.jpg -r 15 -y security.mp4
```


##DEDICATED VIDEO LOOPER FOR RASPI:


[Git - pi_video_looper](https://github.com/adafruit/pi_video_looper)


[Installation](https://learn.adafruit.com/raspberry-pi-video-looper/installation)


**Install Commands:**
```
sudo apt-get update
sudo apt-get install -y git
git clone https://github.com/adafruit/pi_video_looper.git
cd pi_video_looper
sudo ./install.sh
```

####Raspberry Pi Video Looper
Full information:
https://videolooper.de/