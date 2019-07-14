/********************************************************************************/
/* Filename	: Hex_Keypad.c			                                        	*/
/*                                                                      		*/
/* Brief description : 	Hex Keypad control software        						*/
/*                                                                      		*/
/* Programmer         Date       	Version     Comments  		Processor  		*/
/* -----------------------------------------------------------------------------*/
/* Wayne Rabe       09/04/2008  	0.A			MPLAB			18F4550	  		*/
/* Antony Smith		14/03/2013		0.B			AVR Studio		AT32UC3A0512	*/
/********************************************************************************/
#include "gpio.h"
#include "user_board.h"
#include "Hex_Keypad.h"


#include <string.h>
#include <stdio.h>
#include <stdlib.h>

/********************************************************************************/
/*   PRIVATE FUNCTIONS PRIVATE FUNCTIONS PRIVATE FUNCTIONS PRIVATE FUNCTIONS    */
/********************************************************************************/
//void Respond_To_Number_Pressed(unsigned int Key);
//void Respond_To_Quadrant_Pressed(unsigned int Key);

/********************************************************************************/
/*    VARIABLES VARIABLES VARIABLES VARIABLES VARIABLES VARIABLES VARIABLES     */
/********************************************************************************/
unsigned int KeyFunctionsFlags 	= CLEAR;		// defined as 0x00
unsigned int KeyNumberFlags 	= CLEAR;
unsigned short pressed = 0;

/********************************************************************************/
/* Name: Scan_Keypad                                     						*/
/* Description:	Navigational keys Select and Exit								*/
/*				(2C X 3R) + (2C x 2R)											*/
/* Inputs:  void	           									 	        	*/
/* Outputs: void                      	                           				*/
/********************************************************************************/
/*
Q1		- C1 = R1	- 
SELECT	- C1 = R2	- ENTER
RETURN	- C1 = R3	- EXIT
Q2		- C1 = R4	- 

LEFT	- C2 = R1	- LEFT
UP		- C2 = R2	- UP
RIGHT	- C2 = R3	- RIGHT
Q4		- C2 = R4	- 

Q3		- C3 = R1	- 
DOWN	- C3 = R2	- DOWN
*/
bool Scan_Keypad(void) 
{
	unsigned short	ROW_NO  = 0;
	bool			row_pin = false;
	bool			button1 = false;
	
	for(ROW_NO = 0; ROW_NO <= 3; ROW_NO ++)
	{
		row_pin = false;
		switch(ROW_NO)
			{
				case 0:
						gpio_set_pin_low(ROW1);						//column1 = pull down
						row_pin = gpio_get_pin_value(COL1);
						if(!row_pin){Q1_PRESSED_TRUE; KEYPAD_PRESSED_TRUE; while(!ROW1); button1 = true;}
						row_pin = gpio_get_pin_value(COL2);	
						if(!row_pin){LEFT_PRESSED_TRUE; KEYPAD_PRESSED_TRUE; while(!ROW2); button1 = true;}
						row_pin = gpio_get_pin_value(COL3);
						if(!row_pin){Q3_PRESSED_TRUE; KEYPAD_PRESSED_TRUE; while(!ROW3); button1 = true;}
						gpio_set_pin_high(ROW1);					//column1 = release
						break;
				case 1:
						gpio_set_pin_low(ROW2);						//column2 = pull down
						row_pin = gpio_get_pin_value(COL1);	
						if(!row_pin){ENTER_PRESSED_TRUE; KEYPAD_PRESSED_TRUE; while(!ROW1); button1 = true;}
						row_pin = gpio_get_pin_value(COL2);	
						if(!row_pin){TOP_PRESSED_TRUE; KEYPAD_PRESSED_TRUE; while(!ROW2); button1 = true;}
						row_pin = gpio_get_pin_value(COL3);	
						if(!row_pin){BOTTOM_PRESSED_TRUE; KEYPAD_PRESSED_TRUE; while(!ROW3); button1 = true;}
						gpio_set_pin_high(ROW2);					//column2 = release
						break;
				case 2:
						gpio_set_pin_low(ROW3);						//column3 = pull down
						row_pin = gpio_get_pin_value(COL1);	
						if(!row_pin){EXIT_PRESSED_TRUE; KEYPAD_PRESSED_TRUE; while(!ROW1); button1 = true;}
						row_pin = gpio_get_pin_value(COL2);	
						if(!row_pin){RIGHT_PRESSED_TRUE; KEYPAD_PRESSED_TRUE; while(!ROW2); button1 = true;}
						gpio_set_pin_high(ROW3);					//column3 = release
						break;
				case 3:
						gpio_set_pin_low(ROW4);						//column3 = pull down
						row_pin = gpio_get_pin_value(COL1);	
						if(!row_pin){Q3_PRESSED_TRUE; KEYPAD_PRESSED_TRUE; while(!ROW1); button1 = true;}
						row_pin = gpio_get_pin_value(COL2);	
						if(!row_pin){BOTTOM_PRESSED_TRUE; KEYPAD_PRESSED_TRUE; while(!ROW2); button1 = true;}
						gpio_set_pin_high(ROW4);					//column3 = release
						break;
			}
	}
	return button1;
}

/********************************************************************************/
/* Name: Resond_To_Keys                                    						*/
/* Description:	Respond to the key that was pressed			           	        */
/* Inputs:  void	           									 	        	*/
/* Outputs: void                      	                           				*/
/********************************************************************************/
unsigned short Respond_To_Keys() 
{
	//unsigned int i = 0;


	switch(KeyFunctionsFlags)
	{
		case 0x01:
					BOTTOM_PRESSED_FALSE;				// DOWN (2)
					// Move DOWN one block
					pressed = 2;
					//Flash();
					break;
		case 0x02:
					RIGHT_PRESSED_FALSE;				// RIGHT (0)
					// Move RIGHT one block
					pressed = 0;
					//Flash();
					break;
		case 0x04:
					LEFT_PRESSED_FALSE;					// LEFT (1)
					// Move LEFT one block
					pressed = 1;
					//Flash();
					break;
		case 0x08:
					TOP_PRESSED_FALSE;					// UP (3)
					// Move UP one block
					pressed = 3;
					//Flash();
					break;
		case 0x10:
					ENTER_PRESSED_FALSE;				// ENTER (4)
					//Respond_To_Quadrant_Pressed(0);
					pressed = 4;
					//Flash();
					break;
		case 0x20:
					EXIT_PRESSED_FALSE;					// EXIT (5)
					//Respond_To_Quadrant_Pressed(1);
					pressed = 5;
					//Flash();
					break;
		case 0x40:
					Q1_PRESSED_FALSE;
					//Respond_To_Quadrant_Pressed(2);
					pressed = 6;
					//Flash();
					break;
		case 0x80:
					Q2_PRESSED_FALSE;
					//Respond_To_Quadrant_Pressed(3);
					pressed = 6;
					//Flash();
					break;
		case 0x03:
					Q3_PRESSED_FALSE;
					//Respond_To_Quadrant_Pressed(3);
					pressed = 6;
					//Flash();
					break;
		case 0x06:
					Q4_PRESSED_FALSE;
					//Respond_To_Quadrant_Pressed(3);
					pressed = 6;
					//Flash();
					break;
	}
	return pressed;
}

/*
void chill(void)
{
  volatile int i;
  for(i = 0 ; i < 20000; i++);		// +/- 100 milliseconds
}

void Flash(void)					// Green
{
	int b = 0;
	
	for (int x=0; x<=2; x++)
	{
		gpio_tgl_gpio_pin(LED1);
		
		for (b=0; b<25; b++)	// b<25
		{
			chill();
		}
	}	
}*/


