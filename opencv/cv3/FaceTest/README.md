Run the code like this:
-----------------------
(depending on cascade argument):
--------------------------------

python2 face1.py

-OR-

python2 face2.py gr0.jpg

-OR-

python3 face3.py

--------------------------------------------------------
ACCURACY OF THE FACE COUNT:
--------------------------------------------------------
'gr0.jpg' - scaleFactor=1.075,
'gr1.jpg' - scaleFactor=1.12,
--------------------------------------------------------

If you want to understand how the code works, the details are here:

https://realpython.com/blog/python/face-recognition-with-python/


Update: Now supports OpenCV3. This change has been made by furetosan 
(https://github.com/furetosan) and tested on Linux.

To run the OpenCV3 version, run facedetect_cv3.py.

--------------------------------------------------------

Change the parameters & setting the scaleFactor to 1.2 can get rid of the wrong face detection.

