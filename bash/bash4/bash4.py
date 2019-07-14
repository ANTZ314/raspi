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
	command = subprocess.Popen("./bash_file.sh")
	command.wait()
	print(command.stdout)
		
if __name__ == "__main__": main()
