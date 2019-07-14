/********************************************************************************/
/* Filename	: Hex_Keypad.c			                                        	*/
/*                                                                      		*/
/* Brief description : 	Hex Keypad control software        						*/
/*                                                                      		*/
/* Programmer         Date       	Version     Comments  		Processor  		*/
/* -----------------------------------------------------------------------------*/
/* Wayne Rabe       09/04/2008  	0.A			MPLAB			18F4550	  		*/
/* Antony Smith		22/01/2013		0.B			AVR Studio		AT32UC3A0512	*/
/********************************************************************************/

//#include "P18F4550.h"
//#include "Typedef.h"
//#include "main.h"
//#include "Images.h"

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
//unsigned int Q_FLAG 			= CLEAR;


/********************************************************************************/
/* Name: Scan_Keypad                                     						*/
/* Description:	Navigational keys Select and Exit	(3 Columns X 4 Rows)		*/
/* Inputs:  void	           									 	        	*/
/* Outputs: void                      	                           				*/
/********************************************************************************/
/*

Add 1	- C1 = R1
SELECT	- C1 = R2
RETURN	- C1 = R3
Add 2	- C1 = R4

LEFT	- C2 = R1
UP		- C2 = R2
RIGHT	- C2 = R3
Add 4	- C2 = R4

Add 3	- C3 = R1
DOWN	- C3 = R2

*/
void Scan_Keypad(void) 
{
	unsigned short	ROW_NO  = 0;
	bool			row_pin = 0;
	
	for(ROW_NO = 0; ROW_NO <= 2; ROW_NO ++)
	{
		row_pin = false;
		switch(ROW_NO)
			{
				case 0:
						gpio_set_pin_low(COL1);						//column1 = pull down
						row_pin = gpio_get_pin_value(ROW1);
						if(!row_pin){Q1_PRESSED_TRUE; KEYPAD_PRESSED_TRUE; while(!ROW1);}
						row_pin = gpio_get_pin_value(ROW2);	
						if(!row_pin){ENTER_PRESSED_TRUE; KEYPAD_PRESSED_TRUE; while(!ROW2);}
						row_pin = gpio_get_pin_value(ROW3);
						if(!row_pin){EXIT_PRESSED_TRUE; KEYPAD_PRESSED_TRUE; while(!ROW3);}
						row_pin = gpio_get_pin_value(ROW4);	
						if(!row_pin){Q2_PRESSED_TRUE; KEYPAD_PRESSED_TRUE; while(!ROW4);}
						gpio_set_pin_high(COL1);					//column1 = release
						break;
				case 1:
						gpio_set_pin_low(COL2);						//column2 = pull down
						row_pin = gpio_get_pin_value(ROW1);	
						if(!row_pin){LEFT_PRESSED_TRUE; KEYPAD_PRESSED_TRUE; while(!ROW1);}
						row_pin = gpio_get_pin_value(ROW2);	
						if(!row_pin){TOP_PRESSED_TRUE; KEYPAD_PRESSED_TRUE; while(!ROW2);}
						row_pin = gpio_get_pin_value(ROW3);	
						if(!row_pin){RIGHT_PRESSED_TRUE; KEYPAD_PRESSED_TRUE; while(!ROW3);}
						row_pin = gpio_get_pin_value(ROW4);	
						if(!row_pin){Q4_PRESSED_TRUE; KEYPAD_PRESSED_TRUE; while(!ROW4);}
						gpio_set_pin_high(COL2);					//column2 = release
						break;
				case 2:
						gpio_set_pin_low(COL3);						//column3 = pull down
						row_pin = gpio_get_pin_value(ROW1);	
						if(!row_pin){Q3_PRESSED_TRUE; KEYPAD_PRESSED_TRUE; while(!ROW1);}
						row_pin = gpio_get_pin_value(ROW2);	
						if(!row_pin){BOTTOM_PRESSED_TRUE; KEYPAD_PRESSED_TRUE; while(!ROW2);}
						//if(ROW3){THREE_PRESSED_TRUE; KEYPAD_PRESSED_TRUE; while(!ROW3);}
						//if(ROW4){FOUR_PRESSED_TRUE; KEYPAD_PRESSED_TRUE; while(!ROW4);}
						gpio_set_pin_high(COL3);					//column3 = release
						break;
			}
	}
}

/********************************************************************************/
/* Name: Resond_To_Keys                                    						*/
/* Description:	Respond to the key that was pressed			           	        */
/* Inputs:  void	           									 	        	*/
/* Outputs: void                      	                           				*/
/********************************************************************************/
void Respond_To_Keys(void) 
{
	//unsigned int i = 0;


	switch(KeyFunctionsFlags)
	{
		case 0x01:
					BOTTOM_PRESSED_FALSE;
					// Move DOWN one block
					Flash();
					break;
		case 0x02:
					RIGHT_PRESSED_FALSE;
					// Move RIGHT one block
					
					break;
		case 0x04:
					LEFT_PRESSED_FALSE;
					// Move LEFT one block
					Flash();
					break;
		case 0x08:
					TOP_PRESSED_FALSE;
					// Move UP one block
					Flash();
					break;
		case 0x10:
					Q1_PRESSED_FALSE;
					//Respond_To_Quadrant_Pressed(0);
					Flash();
					break;
		case 0x20:
					Q2_PRESSED_FALSE;
					//Respond_To_Quadrant_Pressed(1);
					Flash();
					break;
		case 0x40:
					Q3_PRESSED_FALSE;
					//Respond_To_Quadrant_Pressed(2);
					Flash();
					break;
		case 0x80:
					Q4_PRESSED_FALSE;
					//Respond_To_Quadrant_Pressed(3);
					Flash();
					break;
	}
	/*switch(KeyNumberFlags)
	{
		case 0x01:
					ONE_PRESSED_FALSE;
					Respond_To_Number_Pressed(0);
					break;
		case 0x02:
					TWO_PRESSED_FALSE;
					Respond_To_Number_Pressed(1);
					break;
		case 0x04:
					THREE_PRESSED_FALSE;
					Respond_To_Number_Pressed(2);
					break;
		case 0x08:
					FOUR_PRESSED_FALSE;
					Respond_To_Number_Pressed(3);
					break;
		case 0x10:
					FIVE_PRESSED_FALSE;
					Respond_To_Number_Pressed(4);
					break;
		case 0x20:
					SIX_PRESSED_FALSE;
					Respond_To_Number_Pressed(5);
					break;
		case 0x40:
					SEVEN_PRESSED_FALSE;
					Respond_To_Number_Pressed(6);
					break;
		case 0x80:
					EIGHT_PRESSED_FALSE;
					Respond_To_Number_Pressed(7);
					break;
	}*/
}

void chill(void)
{
  volatile int i;
  for(i = 0 ; i < 20000; i++);		// +/- 100 milliseconds
}

void Flash(void)					// Red
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
}

/*
/ ******************************************************************************** /
/ * Name: Respond_To_Number_Pressed                         						* /
/ * Description:	Reacts to number key pressed				           	        * /
/ * Inputs:  Key		           									 	        	* /
/ * Outputs: void                      	                           				* /
/ ******************************************************************************** /
void Respond_To_Number_Pressed(unsigned int Key)
{
	/ *Quadrant[Q_FLAG].PDigit1[Key] = Digit1;
	Quadrant[Q_FLAG].PDigit2[Key] = Digit2;
	Quadrant[Q_FLAG].PDigit3[Key] = Digit3;
	Quadrant[Q_FLAG].PValue[Key]  = ProbeTemp;
	if(PROBE_SIGN){Quadrant[Q_FLAG].PSign[Key] = 1;}
	else{Quadrant[Q_FLAG].PSign[Key] = 0;}
	UpdateSmallValue(VALUE_IMAGE_X_ORG[Key],VALUE_IMAGE_Y_ORG, Quadrant[Q_FLAG].PDigit3[Key], Quadrant[Q_FLAG].PDigit2[Key], Quadrant[Q_FLAG].PDigit1[Key], Quadrant[Q_FLAG].PValue[Key], Quadrant[Q_FLAG].PSign[Key]);
	ProbeTemp = CLEAR;
	SignCorrected = CLEAR;
	ProbeVoltage = CLEAR;* /	
}


/ ******************************************************************************** /
/ * Name: Respond_To_Quadrant_Pressed                       						* /
/ * Description:	Reacts to quadrant key pressed				           	        * /
/ * Inputs:  Key		           									 	        	* /
/ * Outputs: void                      	                           				* /
/ ******************************************************************************** /
void Respond_To_Quadrant_Pressed(unsigned int Key)
{
	unsigned int i = 0;

	//DisplayImage((rom const u8*)((&CurrentQuadrant[Key])), MAIN_IMAGE_X_ORG, MAIN_IMAGE_Y_ORG, MAIN_IMAGE_WIDTH, (MAIN_IMAGE_HEIGHT / 8));
	for(i = 0; i <= 7; i++)
	{
		//UpdateSmallValue(VALUE_IMAGE_X_ORG[i],VALUE_IMAGE_Y_ORG, Quadrant[Q_FLAG].PDigit3[i], Quadrant[Key].PDigit2[i], Quadrant[Key].PDigit1[i], Quadrant[Key].PValue[i], Quadrant[Key].PSign[i]);
	}
}*/


