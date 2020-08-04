"""
Description:
2 Examples of creating JSON strings from Python Class Object
"""

"""
-------------------------------------------
Convert Python Class Object to JSON string
-------------------------------------------
"""

import json

class Laptop:
	name = 'My Laptop'
	processor = 'Intel Core'
		
#create object
laptop1 = Laptop()
laptop1.name = 'Dell Alienware'
laptop1.processor = 'Intel Core i7'

#convert to JSON string
jsonStr = json.dumps(laptop1.__dict__)

#print json string
print(jsonStr)

"""
--------------------------------------------------------
Convert Properties of Python Class Object to JSON string
--------------------------------------------------------
"""
import json

class Laptop:
	def __init__(self, name, processor, hdd, ram, cost):
		self.name = name
		self.processor = processor
		self.hdd = hdd
		self.ram = ram
		self.cost = cost
		
#create object
laptop1 = Laptop('Dell Alienware', 'Intel Core i7', 512, 8, 2500.00)

#convert to JSON string
jsonStr = json.dumps(laptop1.__dict__)

#print json string
print(jsonStr)