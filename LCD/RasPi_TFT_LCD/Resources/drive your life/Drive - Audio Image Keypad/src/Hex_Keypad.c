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
void Scan_Keypad(void);
void Respond_To_Keys(void);
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
/* Description:	Service the message received from the GPS           	        */
/* Inputs:  void	           									 	        	*/
/* Outputs: void                      	                           				*/
/********************************************************************************/
void Scan_Keypad(void) 
{
	unsigned int ROW_NO = 0;
	
	for(ROW_NO = 0; ROW_NO <= 3; ROW_NO ++)
	{
		switch(ROW_NO)
			{
				case 0:
						gpio_set_pin_high(ROW_0);							//ROW_0 = 1;
						if(COL_0){BOTTOM_PRESSED_TRUE; KEYPAD_PRESSED_TRUE; while(COL_0);}
						if(COL_1){RIGHT_PRESSED_TRUE; KEYPAD_PRESSED_TRUE; while(COL_1);}
						if(COL_2){LEFT_PRESSED_TRUE; KEYPAD_PRESSED_TRUE; while(COL_2);}
						if(COL_3){TOP_PRESSED_TRUE; KEYPAD_PRESSED_TRUE; while(COL_3);}
						gpio_set_pin_low(ROW_0);							//ROW_0 = 0;
						break;
				case 1:
						gpio_set_pin_high(ROW_1);							//ROW_1 = 1;
						if(COL_0){Q1_PRESSED_TRUE; KEYPAD_PRESSED_TRUE; while(COL_0);}
						if(COL_1){Q2_PRESSED_TRUE; KEYPAD_PRESSED_TRUE; while(COL_1);}
						if(COL_2){Q3_PRESSED_TRUE; KEYPAD_PRESSED_TRUE; while(COL_2);}
						if(COL_3){Q4_PRESSED_TRUE; KEYPAD_PRESSED_TRUE; while(COL_3);}
						gpio_set_pin_low(ROW_1);							//ROW_1 = 0;
						break;
				case 2:
						gpio_set_pin_high(ROW_2);							//ROW_2 = 1;
						if(COL_0){ENTER_PRESSED_TRUE; KEYPAD_PRESSED_TRUE; while(COL_0);}
						if(COL_1){EXIT_PRESSED_TRUE; KEYPAD_PRESSED_TRUE; while(COL_1);}
						//if(COL_2){THREE_PRESSED_TRUE; KEYPAD_PRESSED_TRUE; while(COL_2);}
						//if(COL_3){FOUR_PRESSED_TRUE; KEYPAD_PRESSED_TRUE; while(COL_3);}
						gpio_set_pin_low(ROW_2);							//ROW_2 = 0;
						break;
				case 3:
						gpio_set_pin_high(ROW_3);							//ROW_3 = 1;
						//if(COL_0){FIVE_PRESSED_TRUE; KEYPAD_PRESSED_TRUE; while(COL_0);}
						//if(COL_1){SIX_PRESSED_TRUE; KEYPAD_PRESSED_TRUE; while(COL_1);}
						//if(COL_2){SEVEN_PRESSED_TRUE; KEYPAD_PRESSED_TRUE; while(COL_2);}
						//if(COL_3){EIGHT_PRESSED_TRUE; KEYPAD_PRESSED_TRUE; while(COL_3);}
						gpio_set_pin_low(ROW_3);							//ROW_3 = 0;
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
					break;
		case 0x02:
					RIGHT_PRESSED_FALSE;
					// Move RIGHT one block
					break;
		case 0x04:
					LEFT_PRESSED_FALSE;
					// Move LEFT one block
					break;
		case 0x08:
					TOP_PRESSED_FALSE;
					// Move UP one block
					break;
		case 0x10:
					Q1_PRESSED_FALSE;
					//Respond_To_Quadrant_Pressed(0);
					break;
		case 0x20:
					Q2_PRESSED_FALSE;
					//Respond_To_Quadrant_Pressed(1);
					break;
		case 0x40:
					Q3_PRESSED_FALSE;
					//Respond_To_Quadrant_Pressed(2);
					break;
		case 0x80:
					Q4_PRESSED_FALSE;
					//Respond_To_Quadrant_Pressed(3);
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


