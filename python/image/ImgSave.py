# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 14:59:42 2017

@author: antz
"""

import cv2

def main():
	filename1 = '../pics/gr0.jpg'
	filename2 = 'new.png'
	cam = cv2.VideoCapture(filename1)
	s, img = cam.read()
	cv2.imwrite(filename2, img)
	
	#cv2.namedWindow('gray', 1)
	img = cv2.imread(filename2)
	cv2.imshow('image', img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
