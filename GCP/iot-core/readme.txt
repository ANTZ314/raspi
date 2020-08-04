===================
Folder: 'iot-core':
===================

	Folder: 'iot':
	--------------
		-> Piot-core.py		- Read data from QR code + store to CSV file
							- create JSON string, and publish to MY Google Cloud Platform
							- Includes libraries specific to RasPi
							- Uses my generated 'rsa_private.pem' + roots.pem

		-> iot-core.py		- Converted above for PC test publish
							- removed actual QR read, replaced with text file read
							- create JSON string, and publish to MY Google Cloud Platform
							- Uses my generated 'rsa_private.pem' + roots.pem

		-> iot-siatik.py	- integrated siatik's publish function to my test code
							- Read 'QR' string from text doc "qrCode.txt"
							- Convert to JSON and publish to SIATIK's GC-Platform
							- Uses his supplied 'rsa.pem'

	Folder - 'siatik':
	------------------
		-> publish.py		- Tawanda's (SIATIK) test simulation to publish to SAITIK GC-Platform
							- Uses his supplied 'rsa_private.pem'