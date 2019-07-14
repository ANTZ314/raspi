#ifndef HEX_KEYPAD_H
#define HEX_KEYPAD_H

#include "compiler.h"

/********************************************************************************/
/*     PUBLIC CONSTANTS PUBLIC CONSTANTS PUBLIC CONSTANTS PUBLIC CONSTANTS		*/
/********************************************************************************/
#define CLEAR						0x00;
#define KEYPAD_PRESSED_TRUE			0x00;	// check what defined as

// unsigned int KeyFunctionsFlags 	= CLEAR;		// defined as 0x00
// unsigned int KeyNumberFlags 		= CLEAR;

//unsigned int KeyFunctionsFlags 	= 0x00;		//CLEAR;		// defined as 0x00

/********************************************************************************/
/*  PUBLIC MACRO'S PUBLIC MACRO'S PUBLIC MACRO'S PUBLIC MACRO'S PUBLIC MACRO'S  */
/********************************************************************************/
/*
// Redefined from 'user_board.h'
#define COL_0							AVR32_PIN_PA00
#define COL_1							AVR32_PIN_PA01
#define COL_2							AVR32_PIN_PA02
#define COL_3							AVR32_PIN_PA03

#define ROW_0							AVR32_PIN_PA04
#define ROW_1							AVR32_PIN_PA05
#define ROW_2							AVR32_PIN_PA06
#define ROW_3							AVR32_PIN_PA07
*/
/*
#define ROW_0_ON						(ROW_0 = 1)
#define ROW_0_OFF						(ROW_0 = 0)
#define ROW_1_ON						(ROW_1 = 1)
#define ROW_1_OFF						(ROW_1 = 0)
#define ROW_2_ON						(ROW_2 = 1)
#define ROW_2_OFF						(ROW_2 = 0)
#define ROW_3_ON						(ROW_3 = 1)
#define ROW_3_OFF						(ROW_3 = 0)*/

#define BOTTOM_PRESSED					(KeyFunctionsFlags &   0x01)
#define BOTTOM_PRESSED_TRUE				(KeyFunctionsFlags |=  0x01)
#define BOTTOM_PRESSED_FALSE			(KeyFunctionsFlags &= ~0x01)
#define RIGHT_PRESSED					(KeyFunctionsFlags &   0x02)
#define RIGHT_PRESSED_TRUE				(KeyFunctionsFlags |=  0x02)
#define RIGHT_PRESSED_FALSE				(KeyFunctionsFlags &= ~0x02)
#define LEFT_PRESSED					(KeyFunctionsFlags &   0x04)
#define LEFT_PRESSED_TRUE				(KeyFunctionsFlags |=  0x04)
#define LEFT_PRESSED_FALSE				(KeyFunctionsFlags &= ~0x04)
#define TOP_PRESSED						(KeyFunctionsFlags &   0x08)
#define TOP_PRESSED_TRUE				(KeyFunctionsFlags |=  0x08)
#define TOP_PRESSED_FALSE				(KeyFunctionsFlags &= ~0x08)
#define ENTER_PRESSED					(KeyFunctionsFlags &   0x10)
#define ENTER_PRESSED_TRUE				(KeyFunctionsFlags |=  0x10)
#define ENTER_PRESSED_FALSE				(KeyFunctionsFlags &= ~0x10)
#define EXIT_PRESSED					(KeyFunctionsFlags &   0x20)
#define EXIT_PRESSED_TRUE				(KeyFunctionsFlags |=  0x20)
#define EXIT_PRESSED_FALSE				(KeyFunctionsFlags &= ~0x20)

//Advertisement Keys (x4) 
/*********************************************************************/
#define Q1_PRESSED						(KeyFunctionsFlags &   0x40)
#define Q1_PRESSED_TRUE					(KeyFunctionsFlags |=  0x40)
#define Q1_PRESSED_FALSE				(KeyFunctionsFlags &= ~0x40)
#define Q2_PRESSED						(KeyFunctionsFlags &   0x80)
#define Q2_PRESSED_TRUE					(KeyFunctionsFlags |=  0x80)
#define Q2_PRESSED_FALSE				(KeyFunctionsFlags &= ~0x80)
#define Q3_PRESSED						(KeyFunctionsFlags &   0x03)
#define Q3_PRESSED_TRUE					(KeyFunctionsFlags |=  0x03)
#define Q3_PRESSED_FALSE				(KeyFunctionsFlags &= ~0x03)
#define Q4_PRESSED						(KeyFunctionsFlags &   0x06)
#define Q4_PRESSED_TRUE					(KeyFunctionsFlags |=  0x06)
#define Q4_PRESSED_FALSE				(KeyFunctionsFlags &= ~0x06)
/*********************************************************************/

/********************************************************************************/
/*     PUBLIC VARIABLES PUBLIC VARIABLES PUBLIC VARIABLES PUBLIC VARIABLES 		*/
/********************************************************************************/

//extern unsigned int Q_FLAG;

/********************************************************************************/
/*     PUBLIC FUNCTIONS PUBLIC FUNCTIONS PUBLIC FUNCTIONS PUBLIC FUNCTIONS 		*/
/********************************************************************************/
bool Scan_Keypad(void);
unsigned short Respond_To_Keys(void);
//void Flash(void);
//void chill(void);

#endif