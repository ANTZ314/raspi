//=============================================================
//          WINSTAR Display Co.,Ltd
//    LCM         :WF43F 8 BIT (80-Series)
//    Contraller: SSD1963
//    Author     :Brian lin 2009/04/08
//    history     :
//==============================================================
//=================================
//   parameter  define
//=================================
#include        <reg52.h>
#include        <stdio.h>          // define I/O functions
#include        <INTRINS.H>        // KEIL FUNCTION

#define        Data_BUS         P1
sbit           IC_A0            =P3^0;    // Data/command select L:Command,H:Data
sbit           IC_WR            =P3^7;    // L: Write, H: Read
sbit           IC_RD            =P3^4;    // Data Enable H-->L
sbit           IC_CS            =P3^1;    // L: Chip select
sbit           IC_UD            =P3^5;    //=P3^6;     // L: UP to Down , H: Down to UP
sbit           IC_LR            =P3^2;    // L: Left to Right , H: Right to Left
sbit           IC_RST           =P3^6;    //=P3^5;    // L: RESET
sbit           STP              =P2^0;    // for winstar test board
sbit           S_S              =P2^1;    // for winstar test board

//----------------------------------------------------------------------
void STP_SC(void)
{
unsigned char x,y,z;
z=P2;
P2=z|| 0x03;
  if(S_S == 1)
    {
       do{
           for(x=0;x<255;x++)
              {
               for(y=0;y<255;y++)
                {}}
       P2=z|| 0x03;

          }while(STP == 0);

     }
}


//;******************************************************************************
void Write_Command(unsigned char command)
{

 IC_RD = 1;
 IC_A0 = 0;
 IC_WR = 0;
 IC_CS = 0;
 Data_BUS = command;
 IC_CS = 1;
 IC_WR = 1;


}

//;******************************************************************************
void Write_Data(unsigned char data1)
{

 IC_RD = 1;
 IC_A0 = 1;
 IC_WR = 0;
 IC_CS = 0;
 Data_BUS = data1;
 IC_CS = 1;
 IC_WR = 1;
}
//==============================================================
void Command_Write(unsigned char command,unsigned char data1)
{
Write_Command(command);
Write_Data(data1);
}
//==============================================================
void SendData(unsigned long color)
{
Write_Data((color)>>16);  // color is red
Write_Data((color)>>8);     // color is green
Write_Data(color);        // color is blue

}
//======================================================
// initial
//======================================================
void Initial_SSD1963 (void)
{
IC_RST = 0;
_nop_();
_nop_();
_nop_();
IC_RST = 1;
_nop_();
_nop_();
_nop_();
Write_Command(0x01);     //Software Reset
Write_Command(0x01);
Write_Command(0x01);
Command_Write(0xe0,0x01);    //START PLL
Command_Write(0xe0,0x03);    //LOCK PLL

Write_Command(0xb0);      //SET LCD MODE  SET TFT 18Bits MODE
Write_Data(0x08);         //SET TFT MODE & hsync+Vsync+DEN MODE
Write_Data(0x80);         //SET TFT MODE & hsync+Vsync+DEN MODE
Write_Data(0x01);         //SET horizontal size=480-1 HightByte
Write_Data(0xdf);          //SET horizontal size=480-1 LowByte
Write_Data(0x01);         //SET vertical size=272-1 HightByte
Write_Data(0x0f);         //SET vertical size=272-1 LowByte
Write_Data(0x00);         //SET even/odd line RGB seq.=RGB

Command_Write(0xf0,0x00);   //SET pixel data I/F format=8bit
Command_Write(0x3a,0x60);   // SET R G B format = 6 6 6

//Write_Command(0xe6);      //scan
//Write_Data(0xff);         //

Write_Command(0xe6);         //SET PCLK freq=9MHz  ; pixel clock frequency
Write_Data(0x01);
Write_Data(0x45);
Write_Data(0x47);


Write_Command(0xb4);      //SET HBP,
Write_Data(0x02);         //SET HSYNC Tatol 525
Write_Data(0x0d);
Write_Data(0x00);         //SET HBP 43
Write_Data(0x2b);
Write_Data(0x28);         //SET VBP 41=40+1
Write_Data(0x00);         //SET Hsync pulse start position
Write_Data(0x00);
Write_Data(0x00);         //SET Hsync pulse subpixel start position

Write_Command(0xb6);       //SET VBP,
Write_Data(0x01);         //SET Vsync total 286=285+1
Write_Data(0x1d);
Write_Data(0x00);         //SET VBP=12
Write_Data(0x0c);
Write_Data(0x09);         //SET Vsync pulse 10=9+1
Write_Data(0x00);         //SET Vsync pulse start position
Write_Data(0x00);

Write_Command(0x2a);      //SET column address
Write_Data(0x00);         //SET start column address=0
Write_Data(0x00);
Write_Data(0x01);         //SET end column address=479
Write_Data(0xdf);

Write_Command(0x2b);      //SET page address
Write_Data(0x00);         //SET start page address=0
Write_Data(0x00);
Write_Data(0x01);         //SET end page address=271
Write_Data(0x0f);

Write_Command(0x29);      //SET display on

}
//======================================================
WindowSet(unsigned int s_x,unsigned int e_x,unsigned int s_y,unsigned int e_y)
{
Write_Command(0x2a);      //SET page address
Write_Data((s_x)>>8);         //SET start page address=0
Write_Data(s_x);
Write_Data((e_x)>>8);         //SET end page address=319
Write_Data(e_x);

Write_Command(0x2b);      //SET column address
Write_Data((s_y)>>8);         //SET start column address=0
Write_Data(s_y);
Write_Data((e_y)>>8);         //SET end column address=239
Write_Data(e_y);
}

//=======================================
void FULL_ON(unsigned long dat)
{
unsigned int x,y,z;
WindowSet(0x0000,0x01Df,0x0000,0x010F);
Write_Command(0x2c);
for(x=0;x<272;x++)
   {
        for(y= 0;y<40;y++)
                {
               for(z= 0;z<12;z++)
                  {
                      SendData(dat);
                  }
                }
   }
}
//=======================================
FRAME()
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
 SendData(0xff0000);             //red
   for(i=0;i<239;i++)
   {
      SendData(0x000000);             //black
      SendData(0x000000);             //black
   }
 SendData(0x0000ff);             //blue
  }

 for(j= 0 ;j<40;j++)
  {
   for(i=0;i<12;i++)
   {
    SendData(0xffffff);             //white
   }
  }
}
//=======================================
void main()
{
IC_UD = 0;
IC_LR = 1;
Initial_SSD1963();

while(1)
        {
      //FRAME();
      STP_SC();
        FULL_ON(0xff0000);   // red
      STP_SC();
        FULL_ON(0x00ff00);   // green
      STP_SC();
        FULL_ON(0x0000ff);    // blue
      STP_SC();
        //FULL_ON(0xff00ff);
      STP_SC();
        //FULL_ON(0x00ffff);
      STP_SC();

        }
}

