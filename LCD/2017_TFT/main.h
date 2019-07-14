#ifndef MAIN_H_
#define MAIN_H_


/**************************************
	   Define the LCD Control Pins
 **************************************/
const int IC_A0    = 3;	// L:Command,H:Data		- Broadcom pin xx, P1 pin x
const int IC_WR    = 04; 	// L: Write, H: Read	- Broadcom pin 04, P1 pin 07
const int IC_RD    = 17; 	// Data Enable H-->L 	- Broadcom pin 17, P1 pin 11
const int IC_CS    = 19; 	// L: Chip select		- Broadcom pin 19, P1 pin 35
const int IC_RST   = 26; 	// L: RESET 			- Broadcom pin 26, P1 pin 37
const int BlEn     = 2; 	// PWM Back Light 		- Broadcom pin 02, P1 pin 03
const int DISP_ON  = 21;	// Display On			- Broadcom pin 21, P1 pin 40
const int pwmValue = 75; 	// Use this to set an LED brightness
/**************************************
	   Define the LCD Data Pins
 **************************************/
const int DB0  = 27; 		// Data_00 				- Broadcom pin 27, P1 pin 13
const int DB1  = 22; 		// Data_01 				- Broadcom pin 22, P1 pin 15
const int DB2  = 10; 		// Data_02				- Broadcom pin 10, P1 pin 19
const int DB3  = 9; 		// Data_03  			- Broadcom pin 9,  P1 pin 21
const int DB4  = 11; 		// Data_04  			- Broadcom pin 11, P1 pin 23
const int DB5  = 5; 		// Data_05  			- Broadcom pin 5,  P1 pin 29
const int DB6  = 6; 		// Data_06 				- Broadcom pin 6,  P1 pin 31
const int DB7  = 13; 		// Data_07				- Broadcom pin 13, P1 pin 33
 /**************************************
	   Define all other Pins
 **************************************/
//const int butPin = 17; 	// Active-low button	- Broadcom pin 17, P1 pin 11

/**************************************
	   PROTOTYPES
 **************************************/
int main(void);
void initialise(void);
void Back_Flash(void);

#endif /* MAIN_H_ */
