You can see that wiringPi pin 0 is GPIO-17. wiringPi pin 1 is GPIO-18, wiringPi pin 2 is GPIO-21 an so on. 
To use the GPIO pin numbering then you need to pass the -g flag to the gpio program:

gpio -g write 17 1

gpio -g write 17 0

--------------------

The 2nd Red LED is connected to wiringPi pin 3, (GPIO-22), and the 2nd Green LED is connected to wiringPi pin 4, (GPIO-23).
Test them as before with the gpio command, e.g.

for i in 0 1 2 3 4 ; do gpio mode $i out; done
for i in 0 1 2 3 4 ; do gpio write $i 1; done
for i in 0 1 2 3 4 ; do gpio write $i 0; done

-------------------

We read the button as follows:

gpio mode 8 input
gpio read 8
