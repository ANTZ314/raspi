/******************************************
	Initialize LCD and SSD1963 controller
*******************************************/

/*****************************************************************
NOTE:
* in function "void Initial_SSD1963 (void)"
* (GIMP) with images:	- .bmp format 
						- 24bit RGB 
						- resized to 480x272 pixels

	-> SET ADRRESS MODE (0X36 [line 141])	=> flip horizontal
											=> RGB to BGR invert

*****************************************************************/

#include "gpio.h"
#include "user_board.h"
#include "graphic_lcd.h"

// GLOBALS
#define LARGEST_BYTE 2048;
unsigned int LCD_DB1[8] = {LCD0, LCD1, LCD2, LCD3, LCD4, LCD5, LCD6, LCD7};		// GLOBAL LCD PIN ARRAY
//unsigned int a = 0x00;
int a = 0x00;

//====================================================================================
void Write_Command(unsigned char command)				// SET PLL freq = 113.33MHz -> 9MHz (check)
{
	/*gpio_set_pin_high(IC_RD);			// IC_RD = 1;
	gpio_set_pin_low(IC_A0);			// IC_A0 = 0;
	gpio_set_pin_low(IC_WR);			// IC_WR = 0;
	gpio_set_pin_low(IC_CS);			// IC_CS = 0;
	LCD_Port(command);					// Data_BUS = command;
	gpio_set_pin_high(IC_CS);			// IC_CS = 1;
	gpio_set_pin_high(IC_WR);			// IC_WR = 1;*/
		
	gpio_local_set_gpio_pin(IC_RD);			// IC_RD = 1;
	gpio_local_clr_gpio_pin(IC_A0);			// IC_A0 = 0;
	gpio_local_clr_gpio_pin(IC_WR);			// IC_WR = 0;
	gpio_local_clr_gpio_pin(IC_CS);			// IC_CS = 0;
	LCD_Port(command);					// Data_BUS = command;
	gpio_local_set_gpio_pin(IC_CS);			// IC_CS = 1;
	gpio_local_set_gpio_pin(IC_WR);			// IC_WR = 1;
}
//====================================================================================
void Write_Data(unsigned char data1)
{
	 /*gpio_set_pin_high(IC_RD);			// IC_RD = 1;
	 gpio_set_pin_high(IC_A0);			// IC_A0 = 1;
	 gpio_set_pin_low(IC_WR);			// IC_WR = 0;
	 gpio_set_pin_low(IC_CS);			// IC_CS = 0;
	 LCD_Port(data1);					// Data_BUS = data1;
	 gpio_set_pin_high(IC_CS);			// IC_CS = 1;
	 gpio_set_pin_high(IC_WR);			// IC_WR = 1;*/
	 
	 gpio_local_set_gpio_pin(IC_RD);			// IC_RD = 1;
	 gpio_local_set_gpio_pin(IC_A0);			// IC_A0 = 1;
	 gpio_local_clr_gpio_pin(IC_WR);			// IC_WR = 0;
	 gpio_local_clr_gpio_pin(IC_CS);			// IC_CS = 0;
	 LCD_Port(data1);					// Data_BUS = data1;
	 gpio_local_set_gpio_pin(IC_CS);			// IC_CS = 1;
	 gpio_local_set_gpio_pin(IC_WR);			// IC_WR = 1;
	 
	 //gpio_tgl_gpio_pin(TOP);			// toggling at 64KHz
}
//====================================================================================
void Command_Write(unsigned char command,unsigned char data1)
{
	Write_Command(command);
	Write_Data(data1);
}
//====================================================================================
void SendData(unsigned long color)
{	
	// 24bit -> 8bit sections
	Write_Data((color)>>16);	// color is red		=> 0xFF 00 00
	Write_Data((color)>>8);     // color is green	=> 0x00 FF 00
	Write_Data(color);			// color is blue	=> 0x00 00 FF
}
//====================================================================================
// initialize
//====================================================================================
void Initial_SSD1963 (void)
{
	gpio_set_pin_low(IC_RST);		// IC_RST = 0;
	asm("NOP");
	asm("NOP");
	asm("NOP");

	gpio_set_pin_high(IC_RST);		// IC_RST = 1;
	asm("NOP");
	asm("NOP");
	asm("NOP");

	Write_Command(0x01);			//Software Reset
	Write_Command(0x01);
	Write_Command(0x01);
	Command_Write(0xe0,0x01);		//START PLL
	Command_Write(0xe0,0x03);		//LOCK PLL

	Write_Command(0xb0);			//SET LCD MODE  SET TFT 18Bits MODE
	Write_Data(0x08);				//SET TFT MODE & hsync+Vsync+DEN MODE => [0x0c for 5.7"]
	Write_Data(0x00);				//SET TFT MODE & hsync+Vsync+DEN MODE
	Write_Data(0x01);				//SET horizontal size=480-1 HightByte
	Write_Data(0xdf);				//SET horizontal size=480-1 LowByte
	Write_Data(0x01);				//SET vertical size=272-1 HightByte
	Write_Data(0x0f);				//SET vertical size=272-1 LowByte
	Write_Data(0x00);				//SET even/odd line RGB seq.=RGB
	
// original 18bit -> 6 6 6 format
	Command_Write(0xf0,0x00);		//SET pixel data I/F format = 8bit
	Command_Write(0x3a,0x70);		// SET R G B format = 6 6 6 (24bit)

	Write_Command(0xe2);			//SET PLL freq=113.33MHz
	Write_Data(0x21);				//(0x22);
	Write_Data(0x02);				//(0x03);
	Write_Data(0x54);				// dummy byte //(0x04);

	Write_Command(0xe6);			//SET PCLK freq=9MHz  (pixel clock frequency)
	Write_Data(0x01);				//83271 [E6h notes pg74]
	Write_Data(0x45);
	Write_Data(0x47);

	Write_Command(0xb4);      //SET HBP,
	Write_Data(0x02);         //SET HSYNC Total 525
	Write_Data(0x0d);
	Write_Data(0x00);         //SET HBP 43
	Write_Data(0x2b);
	Write_Data(0x28);         //SET VBP 41=40+1
	Write_Data(0x00);         //SET Hsync pulse start position
	Write_Data(0x00);
	Write_Data(0x00);         //SET Hsync pulse sub-pixel start position

	Write_Command(0xb6);       //SET VBP,
	Write_Data(0x01);         //SET Vsync total 286 = 285 + 1
	Write_Data(0x1d);
	Write_Data(0x00);         //SET VBP=12
	Write_Data(0x0c);
	Write_Data(0x09);         //SET Vsync pulse 10 = 9 + 1
	Write_Data(0x00);         //SET Vsync pulse start position
	Write_Data(0x00);

	Write_Command(0x2a);      //SET column address
	Write_Data(0x00);         //SET start column address = 0
	Write_Data(0x00);
	Write_Data(0x01);         //SET end column address = 479
	Write_Data(0xdf);

	Write_Command(0x2b);      //SET page address
	Write_Data(0x00);         //SET start page address = 0
	Write_Data(0x00);
	Write_Data(0x01);         //SET end page address = 271
	Write_Data(0x0f);

	Write_Command(0x36);	  //Set Address Mode
	Write_Data(0x88);		  //screen right-way up
	//Write_Data(0x0A);		  //screen upside down
	
	Write_Command(0x29);      //SET display on
	Write_Command(0x2c);	  //Write Memory Start

}
//====================================================================================
void WindowSet(unsigned int s_x,unsigned int e_x,unsigned int s_y,unsigned int e_y)
{
	Write_Command(0x2a);      //SET page address
	Write_Data((s_x)>>8);     //SET start page address=0
	Write_Data(s_x);
	Write_Data((e_x)>>8);     //SET end page address=479
	Write_Data(e_x);

	Write_Command(0x2b);      //SET column address
	Write_Data((s_y)>>8);     //SET start column address=0
	Write_Data(s_y);
	Write_Data((e_y)>>8);     //SET end column address=271
	Write_Data(e_y);
}
//====================================================================================
void FULL_ON(unsigned long dat)					// 0xff0000 = red
{
	unsigned int x,y,z;
	WindowSet(0x0000,0x01Df,0x0000,0x010F);		// (0, 479, 0, 271)
	//WindowSet(0x0000,0x013f,0x0000,0x00EF);	// (0, 319, 0, 239)
	Write_Command(0x2c);						// write memory start
	
	for(x=0;x<272;x++)
	   {
			for(y= 0;y<40;y++)
			{
				    for(z= 0;z<12;z++)
					{
						  SendData(dat);		// (12x40x272) = 13560
					}
			}
	   }
}
//====================================================================================
void FRAME(void)
{
	unsigned int i,j;
	
	WindowSet(0x0000,0x01Df,0x0000,0x010F);
	Write_Command(0x2c);
	
	for(j= 0 ;j<40;j++)
	  {
		   for(i=0;i<12;i++)
		   {
				SendData(0xffffff);             //white
		   }
	  }

	 for(j=0;j<270;j++)
	 {
		 SendData(0xff0000);					//red
		   for(i=0;i<239;i++)
		   {
			  SendData(0x000000);				//black
			  SendData(0x000000);				//black
		   }
		 SendData(0x0000ff);					//blue
	  }

	 for(j= 0 ;j<40;j++)
	  {
	   for(i=0;i<12;i++)
	   {
		SendData(0xffffff);						//white
	   }
	  }
}
//==================================================================================*/
/************************************************************************************/
/*								MINE										        */
/************************************************************************************/
//===================================================================================\=
void Image_call (const char * image, long size1, int pic_call)
{
	int x;
//	int y;
	
	// Block one MINUS 1st 54 bytes of BMP data (16 bytes on LCD)
	
	if(pic_call == 1)
	{
		WindowSet(0x0000,0x01Df,0x0000,0x010F);		// (0, 479, 0, 271)
		//WindowSet(0x0000,0x01Df,0x0000,0x010F);	// (0, 479, 0, 271)
		Write_Command(0x2c);						// write memory start
		a = 0x36;									// 54 bytes

		for(x = 0; x < (size1 - 0x36); x++)
	   {		
			Write_Data(image [a]);
			a++;									// 'a' is global
	   }
	   a = 0x00;
	}	
	else{
	   for(x = 0; x < size1; x++)
	   {		
			Write_Data(image [a]);
			a++;									// 'a' is global
	   }
	   a = 0x00;										// reset 'a' -> shifted
	}	   
}
//====================================================================================
// initializes output pins for LCD
void LCD_init(void)
{
	for (int count = 0; count < 8; count++)
	{
		gpio_local_enable_pin_output_driver(LCD_DB1[count]);	// enable pins separately
		gpio_local_clr_gpio_pin(LCD_DB1[count]);				// always clear pin before use
	}	
// Enable LCD control pins as GPIOs
	gpio_local_enable_pin_output_driver(IC_A0);
	gpio_local_enable_pin_output_driver(IC_CS);
	gpio_local_enable_pin_output_driver(IC_RST);
	gpio_local_enable_pin_output_driver(IC_WR);
	gpio_local_enable_pin_output_driver(IC_RD);
// Clear all LCD control GPIOs
	gpio_local_clr_gpio_pin(IC_A0);
	gpio_local_clr_gpio_pin(IC_CS);
	gpio_local_clr_gpio_pin(IC_RST);
	gpio_local_clr_gpio_pin(IC_WR);
	gpio_local_clr_gpio_pin(IC_RD);
	
	//ME
	gpio_enable_gpio_pin(Disp_On);
	gpio_enable_gpio_pin(Bl_En);
	gpio_set_pin_high(Disp_On);
	gpio_set_pin_high(Bl_En);
}
//====================================================================================
// Receives 8 bit value and outputs on LCD Data Bus.
// Masks each bit, then outputs to pin -> 1bit = 6 cycles (1byte = 48 cycles)
void LCD_Port(uint8_t lcd_out)	
{
	unsigned int Temp;
	unsigned int LCD_Mask = 0x01;
	/*
	for (int count = 0; count < 8; count++)
	{
		Temp = lcd_out;
		Temp &= LCD_Mask;
		
		if (Temp >= 0X01)
		{
			// pin matching count = high
			gpio_set_pin_high(LCD_DB1[count]);			// still need to enable and clear each pin initially
		}
		else{
			// pin matching count = low
			gpio_set_pin_low(LCD_DB1[count]);
		}
		
		//LCD_Mask = LCD_Mask << 1;						// shift mask to next bit (double)
		LCD_Mask *= 2;
		
	}*/
	Temp = lcd_out;
	if ((Temp &= 0x01) != 0x01) gpio_local_clr_gpio_pin(LCD_DB1[0]); else gpio_local_set_gpio_pin(LCD_DB1[0]);Temp = lcd_out;
	if ((Temp &= 0x02) != 0x02) gpio_local_clr_gpio_pin(LCD_DB1[1]); else gpio_local_set_gpio_pin(LCD_DB1[1]);Temp = lcd_out;
	if ((Temp &= 0x04) != 0x04) gpio_local_clr_gpio_pin(LCD_DB1[2]); else gpio_local_set_gpio_pin(LCD_DB1[2]);Temp = lcd_out;
	if ((Temp &= 0x08) != 0x08) gpio_local_clr_gpio_pin(LCD_DB1[3]); else gpio_local_set_gpio_pin(LCD_DB1[3]);Temp = lcd_out;
	if ((Temp &= 0x10) != 0x10) gpio_local_clr_gpio_pin(LCD_DB1[4]); else gpio_local_set_gpio_pin(LCD_DB1[4]);Temp = lcd_out;
	if ((Temp &= 0x20) != 0x20) gpio_local_clr_gpio_pin(LCD_DB1[5]); else gpio_local_set_gpio_pin(LCD_DB1[5]);Temp = lcd_out;
	if ((Temp &= 0x40) != 0x40) gpio_local_clr_gpio_pin(LCD_DB1[6]); else gpio_local_set_gpio_pin(LCD_DB1[6]);Temp = lcd_out;
	if ((Temp &= 0x80) != 0x80) gpio_local_clr_gpio_pin(LCD_DB1[7]); else gpio_local_set_gpio_pin(LCD_DB1[7]);Temp = lcd_out;
	
}
//====================================================================================
//LCD_Map
/*
void LCD_Map()
{
	static const gpio_map_t GPIO_MAP =
	{
		{LCD0}, {LCD1},
		{LCD2}, {LCD3},
		{LCD4}, {LCD5},
		{LCD6}, {LCD7}
	};
	
	gpio_enable_module(GPIO_MAP, sizeof(GPIO_MAP) / sizeof(GPIO_MAP[0]));
	
	// For Example
	GPIO_MAP = 0x55;			// error "assignment of read-only variable 'GPIO_MAP'"
	
}*/
//====================================================================================



