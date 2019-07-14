/********************************************************************************/
/* Filename	: main.c	    		                                        	*/
/*                                                                      		*/
/* Brief description : 	Audio and Image Decoding Main File 						*/
/*						LCD used Nu-Vision: 480x272 4.3'						*/
/*						Converted images to 480x272 bitmap files				*/
/*                                                                      		*/
/* Programmer         Date       	Version       	Comments  			      	*/
/* -----------------------------------------------------------------------------*/
/* Antony Smith       20/11/2012  	0.A           	First Code   		      	*/
/********************************************************************************/

/* \ file: Audio UserBoard V2.10
 * \ User Board version of "V2_10" for AT32UC3A0512AU
 * \ Tx SSC output via PDCA -> [GClk 11.2MHz; Clk 1.41MHz; Sync 44100Hz]
 * \ Rx SPI input direct [12-15MHz]
 
 * Available RAM:	512 KBytes
 * Available FLASH:	 64 KBytes
 
 * -> Audio Output is correct -> [16 bit - big endian - 44100 - stereo - raw]
 * -> Input Buttons correct
 * -> Image display works and scrolls between menus and images
 * -> Changed PIN defines to fit new Layout  
 
 * MUST FIX:
 * => Include membrane Keypad Routine...
 */

#include <asf.h>
#include <avr32/io.h>
#include "compiler.h"
#include "user_board.h"
#include "power_clocks_lib.h"
#include "gpio.h"
#include "spi.h"
#include "conf_sd_mmc_spi.h"
#include "sd_mmc_spi.h"
#include "pdca.h"
#include "intc.h"
#include "flashc.h"
#include "fsaccess.h"
#include "sd_mmc_spi_mem.h"
#include "conf_uda1330ats.h"
#include "graphic_lcd.h"

// Dummy char table
const char dummy_data[] =
#include "dummy.h"
;

//--------------------------------------------------------------
//--------------------  G L O B A L S  D E F S  ----------------
//--------------------------------------------------------------
#define AVR32_PDCA_PID_USED_SPI_RX			AVR32_PDCA_PID_SPI0_RX			// SPI 0
#define AVR32_PDCA_PID_USED_SPI_TX			AVR32_PDCA_PID_SPI0_TX
#define AVR32_PDCA_PID_USED_SSC_TX			AVR32_PDCA_PID_SSC_TX
#define AVR32_PDCA_CHANNEL_SPI_RX			2
#define AVR32_PDCA_CHANNEL_SPI_TX			1
#define AVR32_PDCA_CHANNEL_SSC_TX			0

#define SSC_TX_PDCA_IRQ						AVR32_PDCA_IRQ_0
#define SSC_TX_PDCA_INT_LEVEL				AVR32_INTC_INT2

// Local RAM buffers to store data from SD Card and read to I2S
volatile char					ram_buffer1[2048];
volatile char					ram_buffer2[2048];

// Transfer SSC and SPI
volatile Bool					in_transferTx	= 0;		// stop start SSC Tx
volatile Bool					in_buffer		= 0;		// alternating Rx btwn ram_buffer1 & 2
volatile Bool					Tx_buff1		= 0;		// bizy with ram-buff1 send
volatile Bool					Tx_buff2		= 0;		// bizy with ram-buff2 send
//unsigned int					Tx_size;					// global for 'size' of transfer
volatile Bool					Tx1_Sent		= 1;		// Prevent double send
volatile Bool					Tx2_Sent		= 1;		// Prevent double send

// Image and Track changing
unsigned short					im_no			= 0;		//
volatile Bool					menu			= 0;		//
volatile Bool					mode			= 0;		//

// TESTING:
unsigned short					check			= 0;		// check value of ram_buffer[]

//--------------------------------------------------------------
//------------------------  PROTOTYPES   -----------------------
//--------------------------------------------------------------
void wait(void);
void blink_led1(void);
void local_pdca_init(void);
void init_IOs(void);

void next_image(unsigned short keypress);
void Get_Image_file(char * buf, int choice);
int  Image_Decode(char * path);
void sd_reader_init(void);
void stop_play(void);

void Get_Audio_file(char * buf, int choice);
int  Audio_Decode(char * path);

void init_ssc_i2s(void);
bool uda1330_dac_output(void *sample_buffer, size_t sample_length);

//! Output parameters.
static struct
{
  uint8_t num_channels;
  void (*callback)(uint32_t arg);
  uint32_t callback_opt;
} uda1330_output_params =
{
  .num_channels = 0,
  .callback     = NULL,
  .callback_opt = 0
};

//--------------------------------------------------------------
//----------------------  FUNCTIONS  ---------------------------
//--------------------------------------------------------------
//===================================================
// Transfer Interrupt handler
__attribute__((__interrupt__))
static void ssc_tx_int_handler(void)
{	
	if(in_transferTx) 
	{
		// either loading twice -> OR -> double send within pdca_reload (half value?)
		if (!in_buffer && Tx1_Sent)
		{ 
			gpio_set_gpio_pin(TOP);
			pdca_load_channel( AVR32_PDCA_CHANNEL_SSC_TX, (void *)&ram_buffer2, 1024);//2048);	// Tx_size);
			gpio_clr_gpio_pin(TOP);
			Tx_buff1 = false;
			Tx_buff2 = true;
			Tx1_Sent = false;
			Tx2_Sent = true;
		} 
		else if (in_buffer && Tx2_Sent)
		{
			gpio_set_gpio_pin(TOP);
			pdca_load_channel( AVR32_PDCA_CHANNEL_SSC_TX, (void *)&ram_buffer1, 1024);//2048);	// Tx_size);
			gpio_clr_gpio_pin(TOP);
			Tx_buff1 = true;
			Tx_buff2 = false;
			Tx2_Sent = false;
			Tx1_Sent = true;
		}
	}			
//===================================================
	// Disable the SSC Tx
	else if (!in_transferTx)
	{
		//Disable_global_interrupt();
		stop_play();
	}
}

//===================================================
// AUDIO-PLAYER COMMON BASE -> [line 737] 'tlv320aic23b.c'
// The Audio example uses PDCA for copying buffer data to SSC
bool uda1330_dac_output(void *sample_buffer, size_t sample_length)
{
  bool global_interrupt_enabled;

  // SSC channel changed from channel 0 to 2
  if (!(pdca_get_transfer_status(AVR32_PDCA_CHANNEL_SSC_TX) & PDCA_TRANSFER_COUNTER_RELOAD_IS_ZERO))
    return false;

  if (sample_length)
  {
    if (uda1330_output_params.num_channels == 1)					// [line 162-172]
    {
      int16_t *s16_sample_buffer = sample_buffer;
      int i;

      for (i = sample_length - 1; i >= 0; i--)
      {
        s16_sample_buffer[2 * i + 1] =
        s16_sample_buffer[2 * i]     = s16_sample_buffer[i];
      }
    }

    /* The PDCA is not able to synchronize its start of transfer with the SSC
     start of period, so this has to be done by polling the TF pin.
     Not doing so may result in channels being swapped randomly. */
	if ((global_interrupt_enabled = Is_global_interrupt_enabled()))
      Disable_global_interrupt();
	  if (pdca_get_transfer_status(AVR32_PDCA_CHANNEL_SSC_TX) & PDCA_TRANSFER_COMPLETE)
    {
      while (gpio_get_pin_value(SSC_TX_FRAME_SYNC_PIN));
      while (!gpio_get_pin_value(SSC_TX_FRAME_SYNC_PIN));
    }
	//pdca_reload_channel(UDA1330_SSC_TX_PDCA_CHANNEL, sample_buffer, sample_length * 2);
    pdca_load_channel(AVR32_PDCA_CHANNEL_SSC_TX, sample_buffer, sample_length * 2);
	if (global_interrupt_enabled)
      Enable_global_interrupt();
	pdca_enable_interrupt_transfer_complete(AVR32_PDCA_CHANNEL_SSC_TX);
	//pdca_enable_interrupt_reload_counter_zero(AVR32_PDCA_CHANNEL_SSC_TX);
	pdca_enable(AVR32_PDCA_CHANNEL_SSC_TX);
	
	//Tx_buff1 = true;							// bizy with buffer1
	//while(check != 1){blink_led1();}
  }
  return true;
}	

//===================================================
// initialize PDCA options and register channels
void local_pdca_init(void)
{
	// initialize PDCA for SSC Tx channel
	pdca_channel_options_t pdca_options_SSC_TX =
	{
		.addr			= (void *)&ram_buffer1,			// 
		.size			= 2048,							// full packet
		.r_addr			= NULL,
		.r_size			= 0,
		.pid			= AVR32_PDCA_PID_USED_SSC_TX,	// Peripheral ID.
		.transfer_size	= PDCA_TRANSFER_SIZE_HALF_WORD  // PDCA_TRANSFER_SIZE_BYTE		// Tranfer size; 8,16 or 32 bits.
	};
	
	// Init PDCA SSC Tx channel
	pdca_init_channel(AVR32_PDCA_CHANNEL_SSC_TX, &pdca_options_SSC_TX);
	
	Disable_global_interrupt();
	// Enable PDCA interrupt: -> [last one registered is first INT to jump to]
	INTC_register_interrupt( (__int_handler) &ssc_tx_int_handler, AVR32_PDCA_IRQ_0, AVR32_INTC_INT0);
	Enable_global_interrupt();
}

//===================================================
/* Initializes SD/MMC resources: GPIO, SPI and SD */
// Maximum speeds PBA frequency -> PPL0 (62.0928 MHz)
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
    .spi_mode     = 0,		// change data on falling, SCLK normally high -> // was 3,
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
  sd_mmc_spi_init(spiOptions, FPBA_HZ);//FOSC0);	// PBSD_HZ (PLL0 -> 48MHz)
}

//===================================================
void init_ssc_i2s(void)
{
	// defined in "uda1330ats.c"
	static const gpio_map_t SSC_GPIO_MAP =
	{
	  {SSC_TX_CLOCK_PIN,      SSC_TX_CLOCK_FUNCTION     },
	  {SSC_TX_DATA_PIN,       SSC_TX_DATA_FUNCTION      },
	  {SSC_TX_FRAME_SYNC_PIN, SSC_TX_FRAME_SYNC_FUNCTION}
	};
	
	volatile avr32_ssc_t *ssc = SSC;
	
	// Assign GPIO to SSC.
	gpio_enable_module(SSC_GPIO_MAP, sizeof(SSC_GPIO_MAP) / sizeof(SSC_GPIO_MAP[0]));
	
	// SSC initialize in I2S mode. 
	//ssc_i2s_init(ssc, 44100, 8, 8, SSC_I2S_MODE_STEREO_OUT, FPBA_HZ);		// 
	ssc_i2s_init(ssc, 44100, 16, 16, SSC_I2S_MODE_STEREO_OUT, FPBA_HZ);
	
	//ssc_i2s_init(ssc, 11025, 8, 8, SSC_I2S_MODE_STEREO_OUT, FPBA_HZ);
	//ssc_i2s_init(ssc, 11025, 16, 16, SSC_I2S_MODE_STEREO_OUT, FPBA_HZ);
}

//===================================================
void sd_reader_init(void)
{
	// Initialize SD/MMC driver resources: GPIO, SPI and SD/MMC.
	sd_mmc_resources_init();
	
	// Initialize I2S mode -> 16; 44100 Hz; 62.028 MHz [PLL0]
	init_ssc_i2s();

	while ( sd_mmc_spi_mem_check() != OK )
	{
		blink_led1();
	}
	
	// Initialize PDCA.
	local_pdca_init();
}

//===================================================
// Software delay -> was approx 500ms (needs update)
void wait(void)
{
  volatile int i;
  for(i = 0 ; i < 20000; i++);		// +/- 100 milliseconds
}
void init_IOs(void)
{
	//======== initialise test PINS =========//
	// OUTPUTS
	gpio_enable_gpio_pin(LED);
	gpio_clr_gpio_pin(LED);		// On board LED
	
	// INPUTS
	gpio_local_enable_pin_output_driver(TOP);
	gpio_local_enable_pin_output_driver(ENTER);
	gpio_local_enable_pin_output_driver(LEFT);
	gpio_local_enable_pin_output_driver(RIGHT);
	gpio_local_enable_pin_output_driver(BOTTOM);
	gpio_local_enable_pin_output_driver(EXIT);
	
	//gpio_enable_gpio_pin(TOP);
	gpio_clr_gpio_pin(TOP);
	//gpio_enable_gpio_pin(ENTER);	
	gpio_clr_gpio_pin(ENTER);
	//gpio_enable_gpio_pin(LEFT);	
	gpio_clr_gpio_pin(LEFT);
	//gpio_enable_gpio_pin(BOTTOM);	
	gpio_clr_gpio_pin(BOTTOM);
	//gpio_enable_gpio_pin(RIGHT);	
	gpio_clr_gpio_pin(RIGHT);
	//gpio_enable_gpio_pin(EXIT);	
	gpio_clr_gpio_pin(EXIT);
	
	//======== initialise DAC PINS (Static Pin Mode)=========//
	// APPL0  -> GND - permanently
	// APPSEL -> Vdd - permanently
	gpio_enable_gpio_pin(APPL1);
	gpio_clr_gpio_pin(APPL1);			// 44.1KHz De-emphasis -> (LOW - OFF)(HIGH - ON)
	gpio_enable_gpio_pin(APPL2);
	gpio_clr_gpio_pin(APPL2);			// GND
	gpio_enable_gpio_pin(APPL3);
	gpio_clr_gpio_pin(APPL3);			// GND
}
void blink_led1(void)
{
	int b = 0;
	
	for (int x=0; x<=2; x++)
	{
		gpio_tgl_gpio_pin(LED);
		
		for (b=0; b<25; b++)	// b<25
		{
			wait();
		}
	}	
}
void next_image(unsigned short keypress)
{
	char filename1[30];
	char filename2[30];
	
	switch (keypress)
	{
	case 0:											//** RIGHT **
		if (menu == 0 && im_no < 99) im_no++;		// 98 -> 99
		
		else if (menu == 1 && im_no < 3) im_no++;	// menu 1, 2, 3

		break;
	case 1:											//** LEFT **
		if (menu == 0 && im_no > 98) im_no--;		// 99 -> 98
		
		else if (menu == 1 && im_no > 1) im_no--;	// menu 3, 2, 1
		
		break;
	/*case 2:										// UP
			
		break;
	case 3:											// DOWN
			
		break;*/
	case 4:											// ENTER
		if (menu == 0 && im_no == 98)
		{
			mode  = 0;								// LEARN MODE
			menu  = 1;
			im_no = 1;
		}
		else if (menu == 0 && im_no == 99)
		{
			mode  = 1;								// TEST MODE
			menu  = 1;
			im_no = 1;
		}
		// ANSWER MODE
		else if (menu == 1 && mode == 0)
		{
			im_no += 30;							// eg. Answer1 = image 31
			Get_Image_file(filename1, im_no);		// jump to full images for scrolling
			Image_Decode(filename1);				// display image
			Get_Audio_file(filename2, 1);
			Audio_Decode(filename2);				// after image -> play audio
			im_no -= 30;
			check = 1;								// skip redisplaying full image
		}
		// QUESTION MODE
		else if (menu == 1 && mode == 1)
		{
			im_no += 40; 							// eg. Question1 = image 41
			Get_Image_file(filename1, im_no);
			Image_Decode(filename1);				// display image
			Get_Audio_file(filename2, 2);
			Audio_Decode(filename2);				// after image -> play audio
			im_no -= 40;
			check = 1;								// skip redisplaying full image
		}	
		break;
	case 5:											// EXIT
		if (menu == 1)								// Back to main menu
		{
			menu = 0;
			im_no = 98;
		}
		break;
	}
	if (check != 1)
	{
		Get_Image_file(filename1, im_no);
		Image_Decode(filename1);
	}		
	check = 0;
}
void stop_play(void)
{
	char filename1[30];
	
	if (pdca_get_transfer_status(AVR32_PDCA_CHANNEL_SSC_TX) & PDCA_TRANSFER_COMPLETE)
	{
		pdca_disable_interrupt_transfer_complete(AVR32_PDCA_CHANNEL_SSC_TX);
		if (uda1330_output_params.callback_opt & AUDIO_DAC_OUT_OF_SAMPLE_CB)
		  uda1330_output_params.callback(AUDIO_DAC_OUT_OF_SAMPLE_CB);
	}

	if (pdca_get_transfer_status(AVR32_PDCA_CHANNEL_SSC_TX) & PDCA_TRANSFER_COUNTER_RELOAD_IS_ZERO)
	{
		pdca_disable_interrupt_reload_counter_zero(AVR32_PDCA_CHANNEL_SSC_TX);
		if (uda1330_output_params.callback_opt & AUDIO_DAC_RELOAD_CB)
		  uda1330_output_params.callback(AUDIO_DAC_RELOAD_CB);
	}
	
	im_no = 99; 							// eg. Start Menu
	Get_Image_file(filename1, im_no);
	Image_Decode(filename1);	
}

//===================================================
//********************* Main ************************
//===================================================
int main (void)
{	
	bool s = 0;			// LEFT
	bool t = 0;			// RIGHT
 	bool u = 0;			// ENTER
	bool v = 0;			// EXIT
	char filename[30];
	char filename1[30];
	
	board_init();
	
	gpio_local_init();
	init_IOs();
	
	INTC_init_interrupts();
	
	// Switch to PLL operation.
	init_sys_clocks();

	// output 11.2896MHz (from 62 MHz PLL0)
	init_dac_gclk();
	
	// initialize FAT system
	b_fsaccess_init();
	
	// Initialize LCD pins
	LCD_init();
	Initial_SSD1963();
	
	// initialize values in ram_buffer 
	for (check = 0; check < 2048; check++)
	{
		ram_buffer1[check] = 0x00;
		ram_buffer2[check] = 0x00;
	}
	gpio_set_pin_high(LED);
	
	// initialize SD-SPI and PDCA options
	sd_reader_init();

	im_no = 0;								// Display Intro Screen
	Get_Image_file(filename1, im_no);
	Image_Decode(filename1);
		
	u = false;								// wait for 'ENTER' button press
	while (u != 1)
	{	
		u = gpio_get_pin_value(ENTER);		
	}
	u = false;
	
	menu  = 0;								// main menu
	im_no = 98;								// main menu 1
	//Display Main Menu 1
	Get_Image_file(filename1, im_no);
	Image_Decode(filename1);
	
	//q = false;							// UP
	//r = false;							// DOWN
	s = false;								// LEFT
	t = false;								// RIGHT
	u = false;								// ENTER
	v = false;								// ESCAPE
	
	// Loop through button check
	while(1)
	{
		// state machine -> to continuously loop through program.
		/*switch(X_X)
		{
			case 1:
				pin_check();
				break;
			case 2:
				next_image();
				break;
			case 3:
				Audio_Decode();
				break;
			default
				pin_check();
				break;
		}	*/		
		
		blink_led1();
		s = gpio_get_pin_value(RIGHT);
		t = gpio_get_pin_value(LEFT);
		u = gpio_get_pin_value(ENTER);
		v = gpio_get_pin_value(EXIT);
		
		if (s == true)						// move image LEFT
		{
			next_image(0);
			s = false;
		}
		else if (t == true)					// move image RIGHT
		{
			next_image(1);
			t = false;
		}
		else if (u == true)					// SELECT/ENTER
		{
			next_image(4);
			u = false;
		}
		else if (v == true)					// ESCAPE/EXIT
		{
			next_image(5);
			v = false;
		}		
	}		
	
}

//===================================================
// ********** FAT GET FILENAME ******************* //
//===================================================
void Get_Image_file(char * buf, int choice)
 {
	unsigned char i_str = 3;		// unsigned long i_str = 3;
	unsigned short file;
	int k = 0;
	
	unsigned char folder[22];
	unsigned char nameIntro[21]	= "A:/Folder1\\File0.bmp";			// ssc_i2s_init(ssc, 44100, 16, 16, SSC_I2S_MODE_STEREO_OUT, FPBA_HZ);
	unsigned char M_Menu1[21]	= "A:/Folder1\\File1.bmp";
	unsigned char M_Menu2[21]	= "A:/Folder1\\File2.bmp";
	unsigned char Menu1[21]		= "A:/Folder1\\File3.bmp";
	unsigned char Menu2[21]		= "A:/Folder1\\File4.bmp";
	unsigned char Menu3[21]		= "A:/Folder1\\File5.bmp";
	unsigned char Ans1[21]		= "A:/Folder1\\File6.bmp";
	unsigned char Ans2[21]		= "A:/Folder1\\File7.bmp";
	unsigned char Ans3[21]		= "A:/Folder1\\File8.bmp";
	unsigned char Quest1[21]	= "A:/Folder1\\File9.bmp";
	unsigned char Quest2[21]	= "A:/Folder1\\FileA.bmp";
	unsigned char Quest3[21]	= "A:/Folder1\\FileB.bmp";
	unsigned char Test1[21]		= "A:/Folder1\\FileC.bmp";
	//unsigned char folder[21] = "A:/Folder2\\File1.raw";
	
	switch (choice)
	{
	case 98:							// Main Menu 1
		while (k<21)
		{
			folder[k] = M_Menu1[k];
			k++;
		}
		break;
	case 99:							// Main Menu 2
		while (k<21)
		{
			folder[k] = M_Menu2[k];
			k++;
		}
		break;
	case 0:								// Start Screen
		while (k<21)
		{
			folder[k] = nameIntro[k];
			k++;
		}
		break;
	case 1:								// Menu Image 1
		while (k<21)
		{
			folder[k] = Menu1[k];
			k++;
		}
		break;
	case 2:								// Menu Image 2
		while (k<21)
		{
			folder[k] = Menu2[k];
			k++;
		}
		break;
	case 3:								// Menu Image 3
		while (k<21)
		{
			folder[k] = Menu3[k];
			k++;
		}
		break;
	case 31:								// Answer Image 1
		while (k<21)
		{
			folder[k] = Ans1[k];
			k++;
		}
		break;
	case 32:								// Answer Image 2
		while (k<21)
		{
			folder[k] = Ans2[k];
			k++;
		}
		break;
	case 33:								// Answer Image 3
		while (k<21)
		{
			folder[k] = Ans3[k];
			k++;
		}
		break;
	case 41:								// Question Image 1
		while (k<21)
		{
			folder[k] = Quest1[k];
			k++;
		}
		break;
	case 42:								// Question Image 2
		while (k<21)
		{
			folder[k] = Quest2[k];
			k++;
		}
		break;
	case 43:								// Question Image 3
		while (k<21)
		{
			folder[k] = Quest3[k];
			k++;
		} 
		break;
	case 11:								// 320 x 240 5.7" LCD
		while (k<21)
		{
			folder[k] = Test1[k];
			k++;
		} 
		break;
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
//===================================================
void Get_Audio_file(char * buf, int choice)
 {
	unsigned char i_str = 3;		// unsigned long i_str = 3;
	unsigned short file;
	unsigned short k = 0;
	
	unsigned char folder1[22];
	//unsigned char folder[21] = "A:/Folder2\\File1.raw";
	unsigned char Audio1[21] = "A:/Folder2\\File2.raw";
	unsigned char Audio2[21] = "A:/Folder2\\File3.raw";			// ssc_i2s_init(ssc, 44100, 16, 16, SSC_I2S_MODE_STEREO_OUT, FPBA_HZ);
	//unsigned char folder[21] = "A:/Folder2\\File4.raw";
	
	file = false;
 	buf[0] = 'A';
 	buf[1] = ':';
 	buf[2] = '/';
	
	if (choice == 1)
	{
		while (k<21)
		{
			folder1[k] = Audio1[k];
			k++;
		}
	}
	else if (choice == 2)
	{
		while (k<21)
		{
			folder1[k] = Audio2[k];
			k++;
		}
	}
	
	while (file == false)
	{	
		buf[i_str] = folder1[i_str];					// set buf to file name from [3]
		i_str++;
		
		if (i_str == 21)							// text file
		{
			// Add NUL character
			buf[i_str] = '\0';
			file = true;
		}
	}
 }
 
//===================================================
// ********** FAT open file ********************** //
//===================================================
int Audio_Decode(char * path)
{
	char					* ptrFile;
	int						fd, i;
	long					size;
	double					k;
	short					Start_Tx	= 0;
	unsigned int			count		= 0;
	volatile bool			esc			= 0;
	
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
//			ptrFile[0] if file smaller than 2048 bytes
//====================================================================	   
          // Add a null terminating char
          ptrFile[size] = '\0';
		   
//=========================================================================
		}
     }
     else
     {
//=========================================================================			
//			ptrFile[0] if file larger than 2048 bytes -> section
//=========================================================================
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
//=========================================================================			
//							*********** ME ***********
//=========================================================================
			// Add a null terminating character
			//ptrFile[i * FS_SIZE_OF_SECTOR] = '\0';
		   
			count	= 0x00;
		  
				// 0 -> 2048 copied to ram buffers alternately
				if (!in_buffer)
				{
					//gpio_set_gpio_pin(TOP);
					// wait for Tx1 to finish -> 1 = bizy
					// interrupt and reload channel for Tx2 -> then release Tx_buff1
					while (Tx_buff1) ;	
					
					for (count = 0; count < (i * FS_SIZE_OF_SECTOR); count++)	// first sector -> 2047
					{
						ram_buffer1[count] = ptrFile[count];
					}
					//ptrAudio1 = &ram_buffer1;
				}					
				else if (in_buffer)
				{
					// wait for Tx1 to finish -> 1 = bizy
					while (Tx_buff2) ;
					
					for (count = 0; count < (i * FS_SIZE_OF_SECTOR); count++)	// first sector -> 2047
					{
						ram_buffer2[count] = ptrFile[count];
					}
				}
			
			Start_Tx++;
			
			// After 2nd buff full -> start PDC -> SSC Tx
			if(Start_Tx == 2)
			{
				in_transferTx = true;
				// initialize the entire PDC
				uda1330_dac_output((void *)&ram_buffer1, 2048);	// start PDC Tx
			}	
			if (Start_Tx == 999)
			{
				Start_Tx = 3;
			}			
		   
			// Decrease remaining size
			size -= (i * FS_SIZE_OF_SECTOR);
			in_buffer = !in_buffer;								// invert value
			
			// Check for escape 
			esc = gpio_get_pin_value(EXIT);
			if (esc == true)					// move image 
			{
//				stop_play();
//				next_image(5);
				in_transferTx = false;
				esc = false;
			}
         }
       }
/* ==================================================================== *
 *			Finish with the remaining data (less than 1 sector)			*
 *																		*
 *			Must finish last 'size' in Tx also.							*
 * ==================================================================== */
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
//=========================================================================			
//			ptrFile[0] -> finish the final bytes of the file
//=========================================================================
			// Add a null terminating char
			ptrFile[size] = '\0';
			
			// once reaches final data -> disable the PDCA
			in_transferTx = false;
//=========================================================================
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
//===================================================
int Image_Decode(char * path)	
{
	char * ptrFile;
	int fd, i;
	long size;
 	
	int first_call = 0x00;
	double k;
	//int temp; 
	long block;
	//int match_byte[14] = {0x5d, 0x78, 0x5e, 0x78, 0x5e, 0x79, 0x5d, 0x78, 0x5c, 0x77};
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
//====================================================================			
//										Try to perform a single access								
//======================================+=============================
     if ( size < (NB_SECTOR_TO_SEND * FS_SIZE_OF_SECTOR) )				// [size = '833'] < (4 * 512) => '2048'
     {
       if( read(fd, ptrFile, size) != size)
       {
          // Error message: "Reading entire file failed"
		  blink_led1();
       }
        else
        {	   
          // Add a null terminating char
          ptrFile[size] = '\0';
          // Display the buffer to user
		}
     }
     else
     {
//=========================================================================			
//	Display RAW BMP image from card address ->  Size larger than 2048 bytes
//=========================================================================
		// Try to send the biggest frame contained in the file
       for (i = NB_SECTOR_TO_SEND ; i > 0 ; i--)						// 4,3,2,1
       {
         // Get sectors of maximum size
         while(size > i * FS_SIZE_OF_SECTOR)
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
           //**PRINT**

		   block = (i * FS_SIZE_OF_SECTOR);
		   first_call += 1;
		   Image_call(ptrFile, block, first_call);
		   		
		   // Decrease remaining size
           size -= (i * FS_SIZE_OF_SECTOR);
         }
       }
//=========================================================================
// Finish with the few data remaining (less than 1 sector)
//=========================================================================
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
           // Display the buffer to user
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
 //===================================================