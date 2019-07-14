/*
	* Reading SD Card using FAT file system
	  
	* Reads RAW BMP data from Card and outputs it to 
	  the (WINSTAR) LCD -> 4.3" SSD1963 controller (272 x 480)
	  
	* Audio format converted to ...? using ...? 
*/
/*
Hex file:
C:\Users\SmithAD\Desktop\NEW PROCESSOR\Software UC3A\JPEG\LCD_1_RAW\LCD_1\Debug
*/

//== INCLUDES ==//
#include <asf.h>
#include "compiler.h"
#include "preprocessor.h"
#include "user_board.h"
#include "power_clocks_lib.h"
#include "flashc.h"
#include "fsaccess.h"
#include "intc.h"
/****************************
		 SDCard Section 
****************************/
#include "conf_sd_mmc_spi.h"
#include "sd_mmc_spi.h"
#include "sd_mmc_spi_mem.h"
/****************************
		 LCD Section 
****************************/
#include "graphic_lcd.h"

// Dummy char table
const char dummy_data[] = 
#include "dummy.h"
;
//===================================================
//				== DEFINES ==						//
//===================================================
#define BOARD		USER_BOARD
#define PBA_HZ      FOSC0
#define FPBA_HZ		48000000
// PBA clock frequency (Hz)

//! Number of bytes in the receive buffer when operating in slave mode
#define BUFFERSIZE					64
#define AVR32_PDCA_CHANNEL_USED_RX	AVR32_PDCA_PID_SPI0_RX
#define AVR32_PDCA_CHANNEL_USED_TX	AVR32_PDCA_PID_SPI0_TX
#define AVR32_PDCA_CHANNEL_SPI_RX	0		// use the pdca channel 0.
#define AVR32_PDCA_CHANNEL_SPI_TX	1		// use the pdca channel 1.

// PDCA Channel pointer
volatile avr32_pdca_channel_t* pdca_channelrx ;
volatile avr32_pdca_channel_t* pdca_channeltx ;

// Used to indicate the end of PDCA transfer
volatile Bool end_of_transfer;

// Local RAM buffer for the example to store 
// data received from the SD/MMC card
volatile char ram_buffer[1000];

const U8 * stream_jpeg_src_ptr;		// JPEG source pointer
U16 stream_src_size;				// JPEG source size

unsigned int im_no = 0;
//===================================================
//				== PROTOTYPES ==					//
//===================================================
void local_pdca_init(void);
void wait(void);
void init_IOs(void);
void blink_led1(void);
void blink_led2(void);
int  FAT_Decode(char * path);
void Get_filename(char * buf, int incy);

//===================================================
static void fcpu_fpba_configure(void)
{
 // Switch the main clock source to Osc0 (12MHz)
  pm_switch_to_osc0(&AVR32_PM, FOSC0, OSC0_STARTUP);

  // Setup PLL0 on Osc0, mul=10 ,no divisor, lockcount=16: 12Mhzx8 = 96MHz output
  pm_pll_setup(&AVR32_PM,
			   0,  // pll.
               7,   // mul.
               1,   // div.
               0,   // osc.
               16); // lockcount.
			   
  // PLL output VCO frequency is 96MHz.
  // We divide it by 2 with the pll_div2=1 to get a main clock at 48MHz.
  pm_pll_set_option(&AVR32_PM, 
					0,  // pll.
                    1,  // pll_freq.
                    1,  // pll_div2.
                    0); // pll_wbwdisable.
  
  // Enable the PLL0 -> 48 MHz
  pm_pll_enable(&AVR32_PM, 0);
  // Wait until the PLL output is stable.
  pm_wait_for_pll0_locked(&AVR32_PM);
  
  // Set all peripheral clocks to run at master clock rate (PLL0 - 48MHz)
  pm_cksel(&AVR32_PM,
           0,   // pbadiv.
           1,   // pbasel.
           0,   // pbbdiv.
           0,   // pbbsel.
           0,   // hsbdiv=cpudiv
           0);  // hsbsel=cpusel
		   
  // Set one wait-state (WS) for flash controller. 0 WS access is up to 30MHz for HSB/CPU clock.
  // As we want to have 48MHz on HSB/CPU clock, we need to set 1 WS on flash controller.
  flashc_set_wait_state(1);		// needs #include "flashc.h"
  	   
  // Switch the main clock source to PLL0.
  pm_switch_to_clock(&AVR32_PM, AVR32_PM_MCCTRL_MCSEL_PLL0);
}

// pdca_int_handler
static void pdca_int_handler(void)
{
  // Disable all interrupts.
  Disable_global_interrupt();

  // Disable interrupt channel.
  pdca_disable_interrupt_transfer_complete(AVR32_PDCA_CHANNEL_SPI_RX);

  sd_mmc_spi_read_close_PDCA();		//de-selects the SD/MMC memory.
  wait();
  // Disable unnecessary channel
  pdca_disable(AVR32_PDCA_CHANNEL_SPI_TX);
  pdca_disable(AVR32_PDCA_CHANNEL_SPI_RX);

  // Enable all interrupts.
  Enable_global_interrupt();

  end_of_transfer = TRUE;
}
//===================================================
/* Initializes SD/MMC resources: GPIO, SPI and SD/MMC.*/
// Maximum speeds PBA frequency
static void sd_mmc_resources_init(void)
{
  // GPIO pins used for SD/MMC interface
  static const gpio_map_t SD_MMC_SPI_GPIO_MAP =
  {
    {SD_MMC_SPI_SCK_PIN,  SD_MMC_SPI_SCK_FUNCTION },  // SPI Clock.
    {SD_MMC_SPI_MISO_PIN, SD_MMC_SPI_MISO_FUNCTION},  // MISO.
    {SD_MMC_SPI_MOSI_PIN, SD_MMC_SPI_MOSI_FUNCTION},  // MOSI.
    {SD_MMC_SPI_NPCS_PIN, SD_MMC_SPI_NPCS_FUNCTION}   // Chip Select NPCS.
  };

  // SPI options.
  spi_options_t spiOptions =
  {
    .reg          = SD_MMC_SPI_NPCS,		  // Defined in evk1101.h as '1'
    .baudrate     = SD_MMC_SPI_MASTER_SPEED,  // Defined in conf_sd_mmc_spi.h. -> 12Mega
    .bits         = SD_MMC_SPI_BITS,          // Defined in conf_sd_mmc_spi.h. -> 8bit
    .spck_delay   = 0,
    .trans_delay  = 0,
    .stay_act     = 1,
    .spi_mode     = 0,
    .modfdis      = 1
  };

  // Assign I/Os to SPI.
  gpio_enable_module(SD_MMC_SPI_GPIO_MAP,
                     sizeof(SD_MMC_SPI_GPIO_MAP) / sizeof(SD_MMC_SPI_GPIO_MAP[0]));

  // Initialize as master.
  spi_initMaster(SD_MMC_SPI, &spiOptions);

  // Set SPI selection mode: variable_ps, pcs_decode, delay.
  spi_selectionMode(SD_MMC_SPI, 0, 0, 0);

  // Enable SPI module.
  spi_enable(SD_MMC_SPI);

  // Initialize SD/MMC driver with SPI clock (PBA).
  //PBA_HZ); -> was set 12MHz now set at PLL0 -> 48MHz -> can still be 62MHz (ssc speed)
  sd_mmc_spi_init(spiOptions, FPBA_HZ);				
}
//===================================================
void local_pdca_init(void)
{
	// this PDCA channel is used for data reception from the SPI
	pdca_channel_options_t pdca_options_SPI_RX =
	{
		.addr = ram_buffer,						  // memory address. 
												  // We take here the address of the string dummy_data. 
												  // This string is located in the file dummy.h
		.size = 512,                              // transfer counter: here the size of the string
		.r_addr = NULL,                           // next memory address after 1st transfer complete
		.r_size = 0,                              // next transfer counter not used here
		.pid = AVR32_PDCA_CHANNEL_USED_RX,        // select peripheral ID - data are on reception from SPI1 RX line
		.transfer_size = PDCA_TRANSFER_SIZE_BYTE  // select size of the transfer: 8,16,32 bits
	};
	
	pdca_channel_options_t pdca_options_SPI_TX =
	{
		.addr = (void *)&dummy_data,              // memory address.
		                                          // We take here the address of the string dummy_data.
		                                          // This string is located in the file dummy.h
		.size = 512,                              // transfer counter: here the size of the string
		.r_addr = NULL,                           // next memory address after 1st transfer complete
		.r_size = 0,                              // next transfer counter not used here
		.pid = AVR32_PDCA_CHANNEL_USED_TX,        // select peripheral ID - data are on reception from SPI1 RX line
		.transfer_size = PDCA_TRANSFER_SIZE_BYTE  // select size of the transfer: 8,16,32 bits
	};
	
  // Init PDCA transmission channel
  pdca_init_channel(AVR32_PDCA_CHANNEL_SPI_TX, &pdca_options_SPI_TX);

  // Init PDCA Reception channel
  pdca_init_channel(AVR32_PDCA_CHANNEL_SPI_RX, &pdca_options_SPI_RX);

  //! \brief Enable pdca transfer interrupt when completed
  INTC_register_interrupt(&pdca_int_handler, AVR32_PDCA_IRQ_0, AVR32_INTC_INT1);  // pdca_channel_spi1_RX = 0

}
//===================================================
//						== MINE ==				   //
//===================================================
void wait(void)
{
  volatile int i;
  for(i = 0 ; i < 20000; i++);		// +/- 100 milliseconds
}
void init_IOs(void)
{
	//======== initialise test PINS =========//
	// OUTPUTS
	// Outputs
	gpio_enable_gpio_pin(LED1);
	gpio_clr_gpio_pin(LED1);
	gpio_enable_gpio_pin(LED2);
	gpio_clr_gpio_pin(LED2);
	// Input
	gpio_enable_gpio_pin(ENTER);
	// gpio_set_gpio_pin(COL3);		// pull up res -> button to Vss
	gpio_clr_gpio_pin(ENTER);		// only pull down res (6k) -> button to Vdd
}
void blink_led1(void)
{
	int b = 0;
	
	for (int x=0; x<=2; x++)
	{
		gpio_tgl_gpio_pin(LED1);
		
		for (b=0; b<30; b++)
		{
			wait();
		}
	}	
}
void blink_led2(void)
{
	int b = 0;
	
	for (int x=0; x<=2; x++)
	{
		gpio_tgl_gpio_pin(LED2);
		
		for (b=0; b<30; b++)
		{
			wait();
		}
	}	
}
void next_image()
{
	char filename[30];
	
	im_no++;
	if (im_no == 10)
	{
		im_no = 1;
	}
	Get_filename(filename, im_no);
	FAT_Decode(filename);
}
//===================================================
int main (void)
{
	int a = 0x00;
	int intro = 99;
	char filename[30];
	
	board_init();
	
	gpio_local_init();
	init_IOs();
	
	// Initialize clocks and PLLs
	fcpu_fpba_configure();
	
	// Initialize interrupt controller
	INTC_init_interrupts();
	
	// Initialize SD/MMC driver resources: GPIO, SPI and SD/MMC
	sd_mmc_resources_init();

	// initialize FSACCESS mutex and navigators (FAT system)
	b_fsaccess_init();
	
	init_IOs();
	
	// Initialize LCD pins
	LCD_init();
	Initial_SSD1963();
	
	gpio_set_pin_low(LED1);						// test LED1 permanently ON
	gpio_set_pin_high(LED2);					// test LED2 permanently ON
	
	/*while (a != 1)
	{	
		a = gpio_get_pin_value(COL3);			// keep checking for insert (high)
	}
	a = 0x00;*/
	while ( sd_mmc_spi_mem_check() != OK )
	{
		blink_led1();
	}
	
	Get_filename(filename, intro);
	FAT_Decode(filename);	
	
//=================================================================================	
	while (1)
	{
		blink_led2();
		gpio_set_pin_high(Bl_En);
		blink_led2();
		gpio_set_pin_low(Bl_En);
	}
}
//===========================================================================================================
// ********************************************* FAT GET FILENAME **************************************** //
//===========================================================================================================
void Get_filename(char * buf, int incy)
 {
	unsigned long i_str = 3;
	unsigned short file;
	int k = 0;
	unsigned char folder[22];	// = "A:/Folder1\\File1.bmp";
	unsigned char nameIntro[22] = "A:/Folder1\\File0.bmp";
	unsigned char name1[22] = "A:/Folder1\\File1.bmp";
	unsigned char name2[22] = "A:/Folder1\\File2.bmp";
	unsigned char name3[22] = "A:/Folder1\\File3.bmp";
	unsigned char name4[22] = "A:/Folder1\\File4.bmp";
	unsigned char name5[22] = "A:/Folder1\\File5.bmp";
	unsigned char name6[22] = "A:/Folder1\\File6.bmp";
	unsigned char name7[22] = "A:/Folder1\\File7.bmp";
	unsigned char name8[22] = "A:/Folder1\\File8.bmp";
	unsigned char name9[22] = "A:/Folder1\\File9.bmp";
	//unsigned char name10[22] = "A:/Folder1\\File10.bmp";
	
	if (incy == 99)
	{
		while (k<21)
		{
			folder[k] = nameIntro[k];
			k++;
		}
	}
	if (incy == 1)
	{
		while (k<21)
		{
			folder[k] = name1[k];
			k++;
		}
	}
	if (incy == 2)
	{
		while (k<21)
		{
			folder[k] = name2[k];
			k++;
		}
	}
	if (incy == 3)
	{
		while (k<21)
		{
			folder[k] = name3[k];
			k++;
		}
	}
	if (incy == 4)
	{
		while (k<21)
		{
			folder[k] = name4[k];
			k++;
		}
	}
	if (incy == 5)
	{
		while (k<21)
		{
			folder[k] = name5[k];
			k++;
		}
	}
	if (incy == 6)
	{
		while (k<21)
		{
			folder[k] = name6[k];
			k++;
		}
	}
	if (incy == 7)
	{
		while (k<21)
		{
			folder[k] = name7[k];
			k++;
		}
	}
	if (incy == 8)
	{
		while (k<21)
		{
			folder[k] = name8[k];
			k++;
		}
	}
	if (incy == 9)
	{
		while (k<21)
		{
			folder[k] = name9[k];
			k++;
		}
	}
	
	file = false;
	buf[0] = 'A';
 	buf[1] = ':';
 	buf[2] = '/';
 	
	while (file == false)
	{	
		buf[i_str] = folder[i_str];					// set buf to file name from [3]
		i_str++;
		
		if (i_str == 21)							// text file
		{
			// Add NUL character
			buf[i_str] = '\0';
			file = true;
		}
	}
 }
//===========================================================================================================
// ************************************************* FAT READ ******************************************** //
//===========================================================================================================																	// char filename1[90]; -> in main
int FAT_Decode(char * path)								// fsaccess_example_read(filename1);
 {
	char * ptrFile;
	int fd, i;
	long size;
 	
	int first_call = 0x00;
	double k;
	long block;
	// 183906 chars
		
   // Try to open the file
   if ((fd = open(path, O_RDONLY)) < 0)
   {
	 // Error message: "Open failed"
	 blink_led1();
     return (-1);  
   }
 
   // Get file size
   size = fsaccess_file_get_size(fd);
 
   // Allocate a buffer
   ptrFile = malloc((NB_SECTOR_TO_SEND * FS_SIZE_OF_SECTOR) + 1);
 
   // Allocation fails
   if (ptrFile == NULL)
   {
     // Error message: "Malloc failed"
	 blink_led1();
   }
   else
   {
     // Try to perform a single access
     if ( size < (NB_SECTOR_TO_SEND * FS_SIZE_OF_SECTOR) )				// [size = '833'] < (4 * 512) => '2048'
     {
       if( read(fd, ptrFile, size) != size)
       {
          // Error message: "Reading entire file failed"
		  blink_led1();
       }
        else
        {
//====================================================================			
//									Read first 10 bytes of "File1.txt"
//====================================================================	   
          // Add a null terminating char
          ptrFile[size] = '\0';
          // Display the buffer to user
          // print_dbg(ptrFile);										//**PRINT**
		  blink_led2();
		}
     }
     else
     {
		// Try to send the biggest frame contained in the file
       for (i = NB_SECTOR_TO_SEND ; i > 0 ; i--)						// 4,3,2,1
       {
         // Get sectors of maximum size
         while(size > i * FS_SIZE_OF_SECTOR)							// size > 2048
         {
			k = read(fd, ptrFile, i * FS_SIZE_OF_SECTOR);				// check returned size??
			
           // Get the data from file
           if( k !=  i * FS_SIZE_OF_SECTOR)
           {
             // Error message: Reading file block failed"
			 blink_led1();
             
			 // Close file
             close(fd);
             return (-1);
           }
           // Add a null terminating character
           ptrFile[i * FS_SIZE_OF_SECTOR] = '\0';
           // Display buffer content to user
           // **PRINT**
//=========================================================================			
//	Display RAW BMP image from card address ->  Size larger than 2048 bytes
//=========================================================================
		   block = (i * FS_SIZE_OF_SECTOR);
		   first_call += 1;
		   Image_call(ptrFile, block, first_call);
//====================================================================			
		   // Decrease remaining size
           size -= (i * FS_SIZE_OF_SECTOR);
         }
       }
       // Finish with the few data remaining (less than 1 sector)
       if ( size > 0 )
       {
         // Get the data from file system
         if( read(fd, ptrFile, size) != size)
         {
           // Error message: "Reading file end failed"
		   blink_led1();
           
		   // Close file
           close(fd);
           return (-1);
         }
         else
         {
           // Add a null terminating char
           ptrFile[size] = '\0';
           block = size;
           Image_call(ptrFile, block, first_call);
         }
       }
     }
     // Free the buffer
     free(ptrFile);
   }
   // Close file
   close(fd);															// fd = '0'
   return (0);
 }