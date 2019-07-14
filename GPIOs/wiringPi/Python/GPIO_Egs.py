    import wiringpi
    
    ##################
    # SETUP PINS IOs #
    ##################
    
    # GPIO port numbers  
    import wiringpi2 as wiringpi  
    wiringpi.wiringPiSetupGpio()  
    wiringpi.pinMode(25, 0) # sets GPIO 25 to input  
    wiringpi.pinMode(24, 1) # sets GPIO 24 to output  
    wiringpi.pinMode(18, 2) # sets GPIO 18 to PWM mode  
      
    # wiringpi numbers  
    import wiringpi2 as wiringpi  
    wiringpi.wiringPiSetup()  
    wiringpi.pinMode(6, 0) # sets WP pin 6 to input  
    wiringpi.pinMode(5, 1) # sets WP pin 5 to output  
    wiringpi.pinMode(1, 2) # sets WP pin 1 to PWM mode  
      
    # Physical P1 header pin numbers  
    import wiringpi2 as wiringpi  
    wiringPiSetupPhys()  
    wiringpi.pinMode(22, 0) # sets P1 pin 22 to input  
    wiringpi.pinMode(18, 1) # sets P1 pin 18 to output  
    wiringpi.pinMode(12, 2) # sets P1 pin 12 to PWM mode 
    
    ######################################
    # How to Read Inputs with WiringPi 2 #
    ######################################
    wiringpi.digitalRead(25)
    
        if my_input:  
        print "Input on Port 25 is 1"  
        # then you'd code what you want to happen when port 25 is HIGH  
    else:  
        print "Input on Port 25 is 0"  
        # then you'd code what you want to happen when port 25 is LOW  
        
        
    ###########################################
    # How to Write to Outputs with WiringPi 2 #
    ###########################################
    # GPIO port numbers  
    import wiringpi2 as wiringpi  
    from time import sleep  
    
    wiringpi.wiringPiSetupGpio()  
    wiringpi.pinMode(24, 1)      # sets GPIO 24 to output  
    wiringpi.digitalWrite(24, 0) # sets port 24 to 0 (0V, off)  
    sleep(10)                    # wait 10s  
    wiringpi.digitalWrite(24, 1) # sets port 24 to 1 (3V3, on)  
    sleep(10)                    # wait 10s  
    wiringpi.digitalWrite(24, 0) # sets port 24 to 0 (0V, off) 
    
    ###########################
    # Clean up after yourself #
    # GOOD PRACTICE...		  #
    ###########################
    # GPIO port numbers  
	import wiringpi2 as wiringpi  
	from time import sleep  
	
	wiringpi.wiringPiSetupGpio()  
	wiringpi.pinMode(24, 1)      # sets GPIO 24 to output  
	wiringpi.digitalWrite(24, 0) # sets port 24 to 0 (0V, off)  
	sleep(10)  
	wiringpi.digitalWrite(24, 1) # sets port 24 to 1 (3V3, on)  
	sleep(10)  
	wiringpi.digitalWrite(24, 0) # sets port 24 to 0 (0V, off)  
	wiringpi.pinMode(24, 0)      # sets GPIO 24 back to input Mode 
        
    #######################
    # ANOTHER LED EXAMPLE #
    #######################
    import wiringpi2 as wiringpi  
    from time import sleep       # allows us a time delay  
    
    wiringpi.wiringPiSetupGpio()  
    wiringpi.pinMode(24, 1)      # sets GPIO 24 to output  
    wiringpi.digitalWrite(24, 0) # sets port 24 to 0 (0V, off)  
      
    wiringpi.pinMode(25, 0)      # sets GPIO 25 to input  
    try:  
        while True:  
            if wiringpi.digitalRead(25):     # If button on GPIO25 pressed   
                wiringpi.digitalWrite(24, 1) # switch on LED. Sets port 24 to 1 (3V3, on)  
            else:  
                wiringpi.digitalWrite(24, 0) # switch off LED. Sets port 24 to 0 (0V, off)  
            sleep(0.05)                      # delay 0.05s  
      
    finally:  # when you CTRL+C exit, we clean up  
        wiringpi.digitalWrite(24, 0) # sets port 24 to 0 (0V, off)  
        wiringpi.pinMode(24, 0)      # sets GPIO 24 back to input Mode  
        # GPIO 25 is already an input, so no need to change anything
        
        
        
    
