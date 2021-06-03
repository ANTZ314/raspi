"""
Quick create, write & close multiple files
"""

import csv, time, sys

sensorData = {"epoch":159, "heading":555}

with open("file1.csv", "+a") as f:
			w = csv.writer(f)
			w.writerow(sensorData.values())
			
print("WAIT...")
time.sleep(2)
			
			
with open("file2.csv", "+a") as f:
			w = csv.writer(f)
			w.writerow(sensorData.values())

print("Exit")
sys.exit(0)	
