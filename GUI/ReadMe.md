#omnigo
**Description:**

* PCB Counter with count touch-screen display, camera based QR Code reader & real-time count upload to Google Cloud Platform
* GCP MQTT to SIATIK GC-Platform
* Raspberry Pi Zero + PiCamera + APDS9960

**Primary Functions:**
	
GUI functionality:
	
* Widget placement + Colour schemes		- [complete]
* Real-time label udpates (count/info)		- [complete]
* Multi-Threading						- [complete]
* multiple windows in parallel operation		- [complete]
* APDS9960 gesture sensor counting method 	- [complete]
* PiCamera & OPENCV QR Code reading		- [complete]
* Scan Kit & Staff ID + storage method		- [complete]
* Exit code required to leave GUI			- [complete]
* Drop-down menu stage selector			- [complete]
* JSON data format conversion			- [complete]
* Upload data to Google Cloud IoT-Core [SIATIK]	- [complete]
* Indicator LED (counting=GREEN)			- [complete]

**Still to Change:**

* Kit / Staff ID can be scanned any order		- [incomplete]
* Continue counting & Catch up publishes		- [incomplete]
* QR time-out -> back to scan button		- [complete]
* Remove both test functions				- [incomplete]
* Check video frame - FULL SCREEN		- [incomplete]

**Notes:**

* GUI EXIT CODE: 	3529# ('*' to Delete)
* STAGE CODE: 		2580# ('*' to Delete)
* QR-Code scanner:
	* Exits after 3x confirmed QR reads
	* Time-Out after 35 seconds
	* 'q' to exit prematurely

* GCP connectivity requirements:
	* 'jwt_maker.py' to create JWT security key
	* ssl security files: 
		* roots.pem
		* rsa_private.pem

**USAGE:**
	python main.py

#TKinter

[An Introduction to Tkinter](https://pythonspot.com/tk-dropdown-example/)

[Example1:](https://educ8s.tv/raspberry-pi-gui-tutorial-create-your-own-gui-graphical-user-interface-with-tkinter-and-python/)

* **beaut.py** - 
* **fu.py** - 
* **gay.py** - 
* **gui0.py** - 
* **gui1.py** - 
* **gui2.py** - 
* **gui3.py** - 
* **gui4.py** - 
* **gui5.py** - 
* **gui6.py** - 
* **gui7.py** - 
* **gui8.py** - 
* **gui9.py** - 
* **gui10.py** - 
* **Tkinter.py** - 



------------
#QT5:

[Qt5 Raspberry pi LED blink Example C++](https://www.youtube.com/watch?v=lh8lqtgzqYA)

[Raspberry Pi GUI Tutorial](https://www.baldengineer.com/raspberry-pi-gui-tutorial.html)

[Design GUI using PyQt5 on Raspberry Pi](http://embeddedlaboratory.blogspot.com/2018/04/design-gui-using-pyqt5-on-raspberry-pi.html)



###Dependencies:
sudo apt-get update
sudo apt-get install qt5-default pyqt5-dev pyqt5-dev-tools



