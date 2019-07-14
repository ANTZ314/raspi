/*
 * File:   main.c
 * Author: SmithAD
 *
 * Created on September 25, 2013, 1:59 PM
 *
 * Compiler HTC v9.82
 *
 *   ** ERROR CHECK **
 x -> Board A sends byte and displays same byte
 x -> Board B receives byte, displays and sends received success byte '$'
 x -> Board A receives OK byte ('$') and displays "SENT"

     ** ERROR CONTROL **
 x -> if no "OK" received after sending (time out): Display fail
 * -> if not sending/receiveing: pole other boards every second (timer flags)

     ** CHECK SUM **
 x -> Before each send, add: Tx addr + Rx addr + Data bytes = check sum (Tx)
 * -> [sender address], [receiver address], [DATA], [check sum]
 * -> After each receive, add: Tx addr + Rx addr + Data bytes = check sum (Rx)
 * -> Compare check sum Rx with Tx
 * -> If no match: send "FAIL_1"

 *   ** FLOW CONTROL **
 * -> When data sent 'OK' flag goes high
 * -> While this flag is high data can increment, but won't send
 * -> when flag low after receiving 'OK' or time out then data can send again

     ** Diff FAIL responses **
 * -> FAIL_1 => Check sum not match (data error)
 * -> FAIL_2 => No "OK" (connection error)
 * -> FAIL_3 => (flow control error)
 *
 */

/* LCD SCREEN LAYOUT/FORMAT *

    ====================     [2x16]
    ||ADDR: A  DATA: X||
    || RESPONSE: FAIL ||
    ====================
 */

 /*********************************************
				NOTE:
* Single byte represents data within FRAME
* Get received string to display on LCD and check byte by byte.
* use pointer 'str' to to save new string to 'string[]'
* from 'string[]' check each new byte [0]-[15]
* from 'string[]' display string on both LCD's

 *********************************************/

#include <xc.h>

// CONFIG1
#pragma config FOSC = INTOSCIO  // Oscillator Selection bits (INTRC oscillator; port I/O function on both RA6/OSC2/CLKO pin and RA7/OSC1/CLKI pin)
#pragma config WDTE = OFF       // Watchdog Timer Enable bit (WDT disabled)
#pragma config PWRTE = OFF      // Power-up Timer Enable bit (PWRT disabled)
#pragma config MCLRE = ON       // RA5/MCLR/VPP Pin Function Select bit (RA5/MCLR/VPP pin function is MCLR)
#pragma config BOREN = OFF      // Brown-out Reset Enable bit (BOR disabled)
#pragma config LVP = ON         // Low-Voltage Programming Enable bit (RB3/PGM pin has PGM function, Low-Voltage Programming enabled)
#pragma config CPD = OFF        // Data EE Memory Code Protection bit (Code protection off)
#pragma config WRT = OFF        // Flash Program Memory Write Enable bits (Write protection off)
#pragma config CCPMX = RB0      // CCP1 Pin Selection bit (CCP1 function on RB0)
#pragma config CP = OFF         // Flash Program Memory Code Protection bit (Code protection off)
// CONFIG2
#pragma config FCMEN = OFF      // Fail-Safe Clock Monitor Enable bit (Fail-Safe Clock Monitor disabled)
#pragma config IESO = OFF       // Internal External Switchover bit (Internal External Switchover mode disabled)

#include <stdio.h>
#include <stdlib.h>
#include "main.h"

/******************
    Prototypes
 *****************/
void initializers(void);
void USART_Init(void);
void putrs1USART(const char *data);
void putrsUSART(const char *data);
void putByteUSART(unsigned char data);
void Welcome(void);
void Response(void);
void Rx_Clr(void);
void Line2_Clr(void);
void Send_String(void);
//void Write_Line1(void);
//void Write_Line2(void);

/******************
      Globals
 *****************/
//unsigned int PA_Nibble    = 0x00;
unsigned char Send_Addr     = 'B';                    // Store Sender (own) Address
unsigned char Rec_Addr      = 0x00;                   // Store Destination Address
unsigned char temp1, udata;

char string_send[LCDlen];                               // = "123456789abcdef"; // Open string for Rx
char string_rec[LCDlen];                                // Store the received characters
char * str_send;// = string
char * str_rec;// = string
const char welcome[LCDlen]  = "  ** WELCOME ** \0";     // Length 16
const char subject[LCDlen]  = " *** CNW401T ***\0";     // Length 16
const char Line1[LCDlen]    = "ADDR: A  DATA: X\0";     // Length 10
const char Line2[LCDlen]    = " RESPONSE:      \0";     // Length 11
const char Success[LCDlen]  = "SENT!!\0";               // Length 6
const char Fail[LCDlen]     = "FAIL!!\0";               // Length 6
const char Clr_Rsp[LCDlen]  = "      \0";               // Length 6
const char Line_Clr[LCDlen] = "                \0";     // Length 16

bit data_flag   = low;                                  // Data ready to send
bit Flow_Flag   = low;                                  // Flow Control Flag
bit addr_flag   = low;                                  // Toggle between device 1/2/3
bit OK_Flag     = low;                                  // OK byte sent/received
bit time_flag   = low;                                  // 65 000 = approx 2 sec
bit pass_fail   = low;                                  // message sent successfully?
unsigned int checksum = 0x0000;                         // checksum total for send and receive
unsigned short i;                                       // General counter variable

/**********************************
    Processor Port/Pin Initialize
**********************************/
void initializers(void)
{
    /*** set corresponding tris bits to inputs and outputs ***/
	TRISA = 0xE0;               // (MCLRE = Input) (PB1/2 = Inputs)
	TRISB = 0xC4;               // RB2/6/7 (Rx_Pic/PGC/PGD)

	// Clear all Ports
	PORTA = 0X00;
	PORTB = 0X00;

    /* OSC SET UP */
    OSCCON = 0x60;              // IRCF Bits for 4MHz (pg 42)
}

/**************
*   USART     *
**************/
void USART_Init(void)
{
    SPBRG = 12;                 // 19200 baud @ 4MHz
    TXSTA = 0x24;               // setup USART transmit
    RCSTA = 0x90;               // setup USART receive
}

/*********************************
  LCD 4 Bit Interfacing Functions
 *********************************/
void Lcd4_Port(char a)
{
    char temper = 0x00;

    temper = a & 0x0F;              // Set bottom 4 Pins only

	if(temper & 1)
	{LCD4_ON; }                 //pinChange(D4,1);
	else
	{LCD4_OFF; }                //pinChange(D4,0);
    temper = a;
	if(temper & 2)
	{LCD5_ON;   }               //pinChange(D5,1);
	else
	{LCD5_OFF; }                //pinChange(D5,0);
    temper = a;
	if(temper & 4)
        {LCD6_ON;}                  //pinChange(D6,1);
	else
	{LCD6_OFF; }                //pinChange(D6,0);
    temper = a;
	if(temper & 8)
	{LCD7_ON;  }                //pinChange(D7,1);
	else
	{LCD7_OFF;}                 //pinChange(D7,0);

        PORTA = PA_Nibble;
}

void Lcd4_Cmd(char a)
{
	RS = 0;                     //pinChange(RS,0);              // => RS = 0
	EN_ON;                      //pinChange(EN,1);              // => E = 1
        PORTA = PA_Nibble;

	__delay_ms(5);
	Lcd4_Port(a);
        __delay_ms(5);

        EN_OFF;                     //pinChange(EN,0);             // => E = 0
        PORTA = PA_Nibble;
}

void Lcd4_Clear()
{
	Lcd4_Cmd(0);
	Lcd4_Cmd(1);
}

void Lcd4_Set_Cursor(char a, char b)
{
	char temp,z,y;
	if(a == 1)
	{
                temp = 0x80 + b;        // 1000 1010
		z = temp>>4;                    // 1010 1000
		y = (0x80+b) & 0x0F;            // 0000 1010
		Lcd4_Cmd(z);
		Lcd4_Cmd(y);
	}
	else if(a == 2)
	{
                temp = 0xC0 + b;        // 1100 1010
		z = temp>>4;                    // 1010 1100
		y = (0xC0+b) & 0x0F;            // 0100 1010
		Lcd4_Cmd(z);
		Lcd4_Cmd(y);
	}
}

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

void Lcd4_Write_Char(char a)
{
	char temp,y;
	temp = a & 0x0F;
	y = a & 0xF0;

	RS = 1;                     //pinChange(RS,1);             // => RS = 1
	Lcd4_Port(y>>4);            //Data transfer
	EN_ON;                      //pinChange(EN,1);
        PORTA = PA_Nibble;          // Actually set the PIN
	__delay_ms(5);
	EN_OFF;                     //pinChange(EN,0);
	PORTA = PA_Nibble;          // Actually set the PIN
        __delay_ms(5);
	Lcd4_Port(temp);
	EN_ON;                      //pinChange(EN,1);
	PORTA = PA_Nibble;          // Actually set the PIN
        __delay_ms(5);
	EN_OFF;                     //pinChange(EN,0);
	PORTA = PA_Nibble;          // Actually set the PIN
        __delay_ms(5);
}

void Lcd4_Write_String(char *a)
{
	int i;
	for(i=0; i<LCDlen; i++)
            Lcd4_Write_Char(a[i]);
}

void Lcd4_Shift_Right()
{
	Lcd4_Cmd(0x01);
	Lcd4_Cmd(0x0C);
}

void Lcd4_Shift_Left()
{
	Lcd4_Cmd(0x01);
	Lcd4_Cmd(0x08);
}
//End LCD 4 Bit Interfacing Functions
/***********************************
    LCD Write Predefined Strings
***********************************/
void Welcome(void)
{
	//unsigned short i;

	for(i=0;i<11;i++)
 		Lcd4_Write_Char(welcome[i]);
}

void Response(void)
{
    Lcd4_Set_Cursor(2,10);              // Set cursor position: 2-10

    if(pass_fail)
    {
        for(i=0;i<6;i++)                // String length + NULL (\0) ? ?
        {
            Lcd4_Write_Char(Success[i]);
        }
    }
    else if(!pass_fail)
    {
       for(i=0;i<6;i++)                 // String length + NULL (\0) ? ?
       {
           Lcd4_Write_Char(Fail[i]);
       }
    }
}

/* Clear the response -> RESPONSE: XXXX */
void Rx_Clr(void)
{
    Lcd4_Set_Cursor(2,10);              // Set cursor position: 2-10

    for(i=0;i<6;i++)                    // String length + NULL (\0) ? ?
        Lcd4_Write_Char(Clr_Rsp[i]);
}

/* Clear the Entire 2nd Line */
void Line2_Clr(void)
{
    Lcd4_Set_Cursor(2,0);               // Goto start of Line 2

    for(i=0;i<LCDlen;i++)               // String length + NULL (\0) ? ?
        Lcd4_Write_Char(Line_Clr[i]);
}

void blink_LED(void)
{
    LED_ON;
    __delay_ms(100);
    LED_OFF;
    __delay_ms(100);
}

void Send_String(void)
{
    //Send_Addr = 'S';                                      // Own Address ['A'/'B'/'C']

    /* Calculate check sum */
    checksum = Rec_Addr + Send_Addr + temp1  + '&';         //0x41 + 0x26;
    /* Keep checksum value under 255 */
    if(checksum <= 255) {string_send[3] = checksum;}        // max value = 0x01AA
    else {
        checksum -= 0x0100;
        string_send[3] = checksum;
    }

    /* Construct the string to send */
    string_send[0] = Rec_Addr;                              // Destination boards address
    string_send[1] = Send_Addr;                             // Sender, This boards address
    string_send[2] = temp1;                                 // Data Byte
    string_send[3] = checksum;                              // CheckSum (Error Checking)
    string_send[4] = '&';                                   // EndByte

    for(i=0; i<5; i++)
    {
        putByteUSART(string_send[i]);                       // send each byte of the string
        __delay_ms(7);                                      // Receive delay is 5ms
    }
}

/********************
*    MAIN - Board 1 *
*********************/
void main(void)
{
    unsigned int time_out = 0x0000;         // u_int = 65535

    initializers();
    USART_Init();
    Lcd4_Init();

    /* WELCOME MESSAGE */
    //Lcd4_Clear();                           // Clear Screen
    //Lcd4_Write_String(welcome);             // write string
    //Lcd4_Set_Cursor(2,0);                   // Set cursor position: 2-0
    //Lcd4_Write_String(subject);             // write string
    //__delay_ms(3000);                       // Delay 3 Seconds

    /* INITIAL DISPLAY SCREEN */
    Lcd4_Clear();                           // Clear Screen agian
    Lcd4_Set_Cursor(1,0);                   // Set cursor position: 1-0
    Lcd4_Write_String((char*) Line1);       // Write "Transmit: "
    Lcd4_Set_Cursor(2,0);                   // Set cursor position: 2-0
    Lcd4_Write_String((char*) Line2);       // Write " Receive: "

    udata = 'D';                            // Set initial data byte
    Rec_Addr = 'B';                         // set initial receive address
    temp1 = udata;                          // For initial Send_String();

    str_rec = &string_rec[0];               // Pointer to received string[]
    str_send = &string_send[0];             // Pointer to send string[]
    for(i=0; i<LCDlen; i++)
    {
        *str_rec = 'D';                     // clear the string
        str_rec++;                          // inc address
        *str_send = 'K';                    // clear the string
        str_send++;                         // inc address
    }

    /** LOOP **/
	while(1)
    {

            /* Data Select Key */
            if(PB_1)
            {
                    LED_ON;
                    blink_LED();            // Kill a man...
            }
            /* Address Select Key */
            else if(PB_2)
            {
                
            }
    }
            
}

/*****************************
*   USART Transmit Functions *
******************************/
void putrsUSART(const char *data)
{
	do {
		while(!(TXSTA & 0x02));
		TXREG = *data;
	} while( *data++ );
}
void putrs1USART(const char *data)
{
	do {
		while(!TXIF);
		TXREG = *data;
	} while( *data++ );
}
void putByteUSART(unsigned char data)
{
	while(!(TXSTA & 0x02));
	TXREG = data;
}