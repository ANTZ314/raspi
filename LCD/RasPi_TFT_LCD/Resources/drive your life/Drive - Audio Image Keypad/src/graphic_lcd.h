#ifndef GRAPHIC_LCD_H_
#define GRAPHIC_LCD_H_

#include "user_board.h"
#include "gpio.h"
#include "pm.h"
#include "flashc.h"

/*============================ DEFINITIONS ===================================*/
#define SSD1963_WIDTH  	480
#define SSD1963_HEIGHT 	272

/*============================ TYPES =========================================*/

//! Datatype color information. Use this for portability between displays. (5-6-5)
//! bits: 15 14 13 12 11 10 9  8  7  6  5  4  3  2  1  0
//!       R  R  R  R  R  G  G  G  G  G  G  B  B  B  B  B

//! bits: 24 23 22 21 20 19 18 17 16 15 14 13 12 11 10  9  8  7  6  5  4  3  2  1

typedef uint16_t ssd1963_color_t;

//================================= PROTOTYPES ======================================
//! @{
void Write_Command(unsigned char command);
void Write_Data(unsigned char data1);
void Command_Write(unsigned char command,unsigned char data1);
void SendData(unsigned long color);
void Initial_SSD1963 (void);
void WindowSet(unsigned int s_x,unsigned int e_x,unsigned int s_y,unsigned int e_y);
void FULL_ON(unsigned long dat);
void FRAME(void);

void Image_call (const char * image, long size1, int pic_call);	

void LCD_init(void);
void LCD_Port(uint8_t lcd_out);

#endif /* GRAPHIC_LCD_H_ */