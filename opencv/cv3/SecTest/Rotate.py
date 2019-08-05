# -*- coding: utf-8 -*-
"""
Description:
PyImageSearch Surveillance Example edited out DropBox storage

USAGE:
$ python security1.py --conf conf1.json
"""
import numpy as np
import cv2
import sys
import imutils

#-- Get user supplied values --#
imagePath = 'gr1.jpg'

#-- Read the image --#
image = cv2.imread(imagePath)					# load the image path
cv2.imshow("original", image)

# get dimensions and centre
(h, w) = image.shape[:2]
center = (w // 2, h // 2)

# rotate by 90 degrees
M = cv2.getRotationMatrix2D(center, 90, 1.0)
rotated = cv2.warpAffine(image, M, (w, h))
cv2.imshow("90 rotate", rotated)

#rotate by another 90 degrees		- NOT ROTATING
rotate = imutils.rotate(image, 180)
cv2.imshow("Again 90", rotate)
cv2.waitKey(0)
