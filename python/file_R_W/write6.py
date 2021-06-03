# -*- coding: utf-8 -*-
"""
Python 2.7 (virtual env)
If file doesn't exist, file is created
If exists, opens existing file reads & prints contents
Appends 10 new lines
"""
import pandas as pd


def main():
	exists = 0											# append after printing contents

	test_set = pd.read_csv('BTC[10_2018]_test.csv')     # Get the real stock price dataset 
	real_stock_price = test_set.iloc[:,1:2].values      # Get all the rows in column 1
	size = len(real_stock_price)						# Get size of array/list

	try:												# Skip if file doesn't exist
		file = open('test.txt', 'r') 					# Open to read file
		print("File Exists: %d" % size)					# 
		print(real_stock_price)							# 
		#print (file.read())							# Print the contents
		file.close()									# Close the file
	except:
		exists = 1										# Don't append twice if file exists
		file= open("test.txt","a+")						# Create/open file then Append data 
		file.write(str(real_stock_price))				# Print results to text file
		file.close()									# Exit the opened file

	if exists == 0:										# append after printing contents
		file= open("test.txt","a+")						# Create/open file then Append data 
		file.write(str(real_stock_price))				# Print results to text file
		file.close()									# Exit the opened file
	else:												# 
		print ("\nFile Didn't exist... So I just created it!")	# notification		
	
if __name__ == "__main__": main()
