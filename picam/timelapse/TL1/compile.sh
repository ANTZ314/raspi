#!/bin/bash

# Print the date
DATE=$(date +'%Y-%m-%d_%H%M')
date
# Go to pictures folder
cd /home/pi/Pictures/t_lapse

echo "Saving to Video, please wait..."

## Compile into MP4:
#ffmpeg -f image2 -r 1 -i img%03d.jpg -r 15 -s hd1080 -vcodec libx264 timelapse.mp4

## Wait for User
echo "Enter any key to continue..."
#Wait for key press...
read -n 1 x

## Move MP4 to Videos folder:
mv 4.jpg /home/pi/Videos	# /home/antz/Videos
echo "Moved to Videos!"
