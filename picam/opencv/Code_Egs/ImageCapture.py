#================================
CAPTURING A SINGLE FRAME:
#================================

from cv2.cv import *
# Initialize the camera
capture = CaptureFromCAM(0)  # 0 -> index of camera
if capture:     # Camera initialized without any errors
   NamedWindow("cam-test",CV_WINDOW_AUTOSIZE)
   f = QueryFrame(capture)     # capture the frame
   if f:
       ShowImage("cam-test",f)
       WaitKey(0)
DestroyWindow("cam-test")

#To capture video, capture frames in a loop with appropriate waitkey. 
#This method of capturing frames is similar to that of OpenCV 2.1

#================================
VIDEOCAPTURE
CAPTURING A SINGLE FRAME:
#================================

from cv2 import *
# initialize the camera
cam = VideoCapture(0)   # 0 -> index of camera
s, img = cam.read()
if s:    # frame captured without any errors
    namedWindow("cam-test",CV_WINDOW_AUTOSIZE)
    imshow("cam-test",img)
    waitKey(0)
    destroyWindow("cam-test")

#This method is most extensively used to capture frames in OpenCV 2.3.1.
#https://jayrambhia.wordpress.com/2012/05/10/capture-images-and-video-from-camera-in-opencv-2-3-1/