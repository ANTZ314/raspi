/*******************************/
/* DATA PORT TEST - LED Chaser */
/*******************************/
/******************************* 
 * To Complile: 
 * gcc -o DataPort3 DataPort3.c -l wiringPi
 * sudo ./DataPort3
 ******************************/

#include <stdio.h>    		// Used for printf() statements
#include <wiringPi.h> 		// Include WiringPi library!

int main(void);
void initialise(void);
void LCD_Port(unsigned char lcd_out);

/**************************************
	   Define the LCD Data Pins
 **************************************/
const int DB0  = 27; 		// Data_00 			- Broadcom pin 27, P1 pin 13
const int DB1  = 22; 		// Data_01 			- Broadcom pin 22, P1 pin 15
const int DB2  = 10; 		// Data_02			- Broadcom pin 10, P1 pin 19
const int DB3  = 9; 		// Data_03  		- Broadcom pin 09, P1 pin 21
const int DB4  = 11; 		// Data_04  		- Broadcom pin 11, P1 pin 23
const int DB5  = 5; 		// Data_05  		- Broadcom pin 05, P1 pin 29
const int DB6  = 6; 		// Data_06 			- Broadcom pin 06, P1 pin 31
const int DB7  = 13; 		// Data_07			- Broadcom pin 13, P1 pin 33

const int BTN  = 2; 		// Button			- Broadcom pin 02, P1 pin 03

/* Define Data pin Array? */
//unsigned int LCD_DB1[8] = {DB0, DB1, DB2, DB3, DB4, DB5, DB6, DB7};
const int LCD_DB1[8] = {27, 22, 10, 9, 11, 5, 6, 13};

/**************************************
			Main Function 
 **************************************/
int main(void)
{
	unsigned int counter = 0x01;
	
	initialise();
	
	/* Continuous Loop */
    while(1)
    {
            delay(50); 					// Wait...
            counter *= 2;				// increment
            if(counter == 0x100)		// if top
            {
				counter = 0x01;			// reset counter
			}    
			LCD_Port(counter);			// output counter
    }
    return 0;
}

/**************************************
	   Initialise GPIO's
 **************************************/
void initialise(void)
{
	/* Setup stuff: */
    	wiringPiSetupGpio(); 		 	// Initialize wiringPi -- using Broadcom pin numbers

		//pinMode(butPin, INPUT);      	// Set button as INPUT
    	//pullUpDnControl(butPin, PUD_UP); // Enable pull-up resistor on button

    	/* Data Pins */
    	pinMode(DB0, OUTPUT);     		// Set as output
    	pinMode(DB1, OUTPUT);      		// Set as output
    	pinMode(DB2, OUTPUT);     		// Set as output
    	pinMode(DB3, OUTPUT);      		// Set as output
    	pinMode(DB4, OUTPUT);     		// Set as output
    	pinMode(DB5, OUTPUT);      		// Set as output
    	pinMode(DB6, OUTPUT);     		// Set as output
    	pinMode(DB7, OUTPUT);      		// Set as output
    
    	printf("Initialisation Complete!\n Press CTRL+C to quit.\n");
}

/*****************************************************************************
 Receives 8 bit value and outputs on LCD Data Bus.
 Masks each bit, then outputs to pin -> 1bit = 6 cycles (1byte = 48 cycles)
******************************************************************************/
void LCD_Port(unsigned char lcd_out)	
{
	unsigned int DBCnt = 0;
	unsigned char Temp;
	unsigned char LCD_Mask = 0x01;						// 0000 0001
	
	for (DBCnt = 0; DBCnt < 8; DBCnt++)					// loop 8 bit (1 byte)
	{
		Temp = lcd_out;									// copy original each loop
		Temp &= LCD_Mask;								// Mask copy each loop
		
		/* pin matching count = high */
		if (Temp >= 0X01) {
			digitalWrite(LCD_DB1[DBCnt], HIGH); 		// Turn LED[x] ON
		}
		/* pin matching count = low */
		else{
			digitalWrite(LCD_DB1[DBCnt], LOW); 			// Turn LED[x] OFF
		}
		
		//LCD_Mask = LCD_Mask << 1;						// shift mask to next bit (double)
		LCD_Mask *= 2;									// shift mask to next bit (double)
	}
}
