# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 14:59:42 2017
@author: antz
"""

import cv2

def main():
	filename = '../pics/gr0.jpg'
	cam = cv2.VideoCapture(0)
	frame = cam.read()[1]
	cv2.imwrite(filename, frame)

if __name__ == '__main__':
    main()
