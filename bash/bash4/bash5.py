"""
====================
OpenCV and PiCamera:
====================
Run: python2 pivid1.py
-----------------------
"""
# import the necessary packages
import subprocess

def main():
	command = subprocess.Popen("echo", ´"Hello stdout"´, stdout=subprocess.PIPE)
	stdout = process.communicate()[0]
	print("STDOUT:{}".format(stdout))
	
if __name__ == "__main__": main()
