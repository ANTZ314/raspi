/*******************************/
/* DATA PORT TEST - LED Chaser */
/*******************************/
/******************************* 
 * To Complile: 
 * gcc -o 2x16 2x16.c -l wiringPi
 * sudo ./2x16
 ******************************/

#include <stdio.h>    		// Used for printf() statements
#include <wiringPi.h> 		// Include WiringPi library!

/**********************
 *  PROTOTYPES
 **********************/
int main(void);
void initialise(void);
void LCD_Port(unsigned char lcd_out);

void Lcd4_Init()
void Lcd4_Clear()
void Lcd4_Set_Cursor(char a, char b)
void Lcd4_Write_String(char *a)
void Lcd4_Write_Char(char a)
void Lcd4_Port(char a)
void Welcome(void)

/**********************
 *  GLOBAL DEFINES
 **********************/
#define high            1
#define low             0
#define LCDlen          17

/**************************************
	   Define the LCD Data Pins
 **************************************/
// (Register Select - High-Data / Low-Instruction)
const int RS   = 4;			// RS 			- Broadcom pin 04, P1 pin 07
const int E    = 17;		// E (Enable)	- Broadcom pin 17, P1 pin 11
const int DB0  = 27; 		// Data_00 		- Broadcom pin 27, P1 pin 13
const int DB1  = 22; 		// Data_01 		- Broadcom pin 22, P1 pin 15
const int DB2  = 10; 		// Data_02		- Broadcom pin 10, P1 pin 19
const int DB3  = 9; 		// Data_03  	- Broadcom pin 09, P1 pin 21
const int DB4  = 11; 		// Data_04  	- Broadcom pin 11, P1 pin 23
const int DB5  = 5; 		// Data_05  	- Broadcom pin 05, P1 pin 29
const int DB6  = 6; 		// Data_06 		- Broadcom pin 06, P1 pin 31
const int DB7  = 13; 		// Data_07		- Broadcom pin 13, P1 pin 33

const int BTN  = 2; 		// Button			- Broadcom pin 02, P1 pin 03

/*************************
* Define Data pin Array? *
**************************/
//unsigned int LCD_DB1[8] = {DB0, DB1, DB2, DB3, DB4, DB5, DB6, DB7};
const int LCD_DB1[8] = {27, 22, 10, 9, 11, 5, 6, 13};	// According to Broadcom

/**********************
 *  GLOBAL VARIABLES
 **********************/
unsigned int PA_Nibble  = 0x00;							// 4 bit (why int ? ? ? ?)
unsigned short i;										// generic counter
const char welcome[LCDlen]  = "  ** WELCOME ** \0";     // Length 16
const char Line_Clr[LCDlen] = "                \0";     // Length 16

/**************************************
			Main Function 
 **************************************/
int main(void)
{
	unsigned int counter = 0x01;
	
	initialise();							// Initialise the GPIOs
	Lcd4_Init();							// Initialise the LCD
	
	/* INITIAL DISPLAY SCREEN */
    Lcd4_Clear();                           // Clear Screen agian
    Lcd4_Set_Cursor(1,0);                   // Set cursor position: 1-0
    Lcd4_Write_String((char*) Line1);       // Write "Transmit: "
    Lcd4_Set_Cursor(2,0);                   // Set cursor position: 2-0
    Lcd4_Write_String((char*) Line2);       // Write " Receive: "
	
	/* Continuous Loop */
    while(1){ ; }
    
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

/*****************************************************************************
					LCD INTITIALISE AND CONTROL
 *****************************************************************************/
/*********************
 * Initialise the LCD
 *********************/
void Lcd4_Init()
{
	Lcd4_Port(0x00);
	__delay_ms(20);
	/** Reset process from datasheet **/
	Lcd4_Cmd(0x03);
	__delay_ms(5);
	Lcd4_Cmd(0x03);
	__delay_ms(11);
	Lcd4_Cmd(0x03);
	/**********************************/
	Lcd4_Cmd(0x02);
	Lcd4_Cmd(0x02);
	Lcd4_Cmd(0x08);
	Lcd4_Cmd(0x00);
	Lcd4_Cmd(0x0C);
	Lcd4_Cmd(0x00);
	Lcd4_Cmd(0x06);
}

/****************
 * Clear the LCD
 ****************/
void Lcd4_Clear()
{
	Lcd4_Cmd(0);
	Lcd4_Cmd(1);
}

/**************************
 * Set the Cursor Position
***************************/
void Lcd4_Set_Cursor(char a, char b)
{
	char temp,z,y;
	if(a == 1)
	{
        temp = 0x80 + b;        		// 1000 1010
		z = temp>>4;                    // 1010 1000
		y = (0x80+b) & 0x0F;            // 0000 1010
		Lcd4_Cmd(z);
		Lcd4_Cmd(y);
	}
	else if(a == 2)
	{
        temp = 0xC0 + b;        		// 1100 1010
		z = temp>>4;                    // 1010 1100
		y = (0xC0+b) & 0x0F;            // 0100 1010
		Lcd4_Cmd(z);
		Lcd4_Cmd(y);
	}
}
 
 /**********************
 * Write 16 Char String
 ***********************/
void Lcd4_Write_String(char *a)
{
	int i;
	for(i=0; i<LCDlen; i++)
	{
		Lcd4_Write_Char(a[i]);
	}
}

 /*****************************
 * Write each character to LCD
 ******************************/
void Lcd4_Write_Char(char a)
{
	char temp,y;
	temp = a & 0x0F;
	y = a & 0xF0;

	RS = 1;                     // pinChange(RS,1);     // => RS = 1
	Lcd4_Port(y>>4);            // Data transfer
	EN_ON;                      // pinChange(EN,1);
    PORTA = PA_Nibble;      	// Output Nible to PORTA
	delay(5);
	EN_OFF;                     // pinChange(EN,0);
	PORTA = PA_Nibble;          // Output Nible to PORTA
    delay(5);
	Lcd4_Port(temp);
	EN_ON;                      // pinChange(EN,1);
	PORTA = PA_Nibble;          // Output Nible to PORTA
    delay(5);
	EN_OFF;                     // pinChange(EN,0);
	PORTA = PA_Nibble;          // Output Nible to PORTA
    delay(5);
}

/*********************************
  LCD 4 Bit Interfacing Functions
 *********************************/
void Lcd4_Port(char a)
{
    char temper = 0x00;

    temper = a & 0x0F;          	// Set bottom 4 Pins only

	if(temper & 1)
		{LCD4_ON;  }                //pinChange(D4,1);
	else
		{LCD4_OFF; }                //pinChange(D4,0);
    temper = a;
	if(temper & 2)
		{LCD5_ON;  }                //pinChange(D5,1);
	else
		{LCD5_OFF; }                //pinChange(D5,0);
    temper = a;
	if(temper & 4)
		{LCD6_ON;  }              	//pinChange(D6,1);
	else
		{LCD6_OFF; }                //pinChange(D6,0);
    temper = a;
	if(temper & 8)
		{LCD7_ON;  }                //pinChange(D7,1);
	else
		{LCD7_OFF; }                //pinChange(D7,0);

    PORTA = PA_Nibble;				// Output Nible to PORTA
}

/***********************************
    LCD Write Predefined Strings
***********************************/
void Welcome(void)
{
	for(i=0;i<11;i++)
 		Lcd4_Write_Char(welcome[i]);
}
