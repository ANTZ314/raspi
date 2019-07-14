#!/bin/bash

DATE=$(date +'%Y%m%d')

raspivid -o /home/pi/Documents/bash/bashcam/pipics/$DATE.h264 -t 10000
