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
 
 * Backup main -> desktop -> Drive main - V2.10 - 18 Feb 2013.txt
 
 * Available RAM:	512 KBytes
 * Available FLASH:	 64 KBytes
 
 * -> SD Card reading correctly
 * -> Audio Output is correct -> [16 bit - big endian - 44100 - stereo - raw]
 * -> Image display  and menu navigation working.
 * -> PIN defines changed to fit new Layout
 
 * MUST FIX:
 * => Include membrane Keypad Routine...
 * => (manual volume control)
 * => I/O initialize to faster screen update
 * => 12MHz Crystal doesn't seem to be used (independent clock for LCD ?)
 * => digital volume control
 *
 * => navigation	- stop mid-playback
 *					- missing question images
 *					- audio files to match images
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
unsigned short					im_no			= 0;		// number passed to Get_Image_File()
unsigned short					aud_no			= 0;		// number passed to Get_Audio_File()
volatile Bool					menu			= 0;		// Navigate Main Menu OR Sub Menu
volatile Bool					mode			= 0;		// LEARN or TEST

// TESTING:
unsigned short					check			= 0;		// check value of ram_buffer[]
unsigned short					im_X			= 0;		// Sub-Menu X position
unsigned short					im_Y			= 0;		// Sub-Menu Y position

//--------------------------------------------------------------
//------------------------  PROTOTYPES   -----------------------
//--------------------------------------------------------------
void wait(void);
void blink_led1(void);
void blink_led2(void);
void local_pdca_init(void);
void init_IOs(void);

void navigate(unsigned short keypress);
void Get_Image_file(char * buf, int choice);
int  Image_Decode(char * path);
void sd_reader_init(void);
void stop_play(void);

void Get_Audio_file(char * buf, int choice);
int  Audio_Decode(char * path);

void init_ssc_i2s(void);
bool uda1330_dac_output(void *sample_buffer, size_t sample_length);

//! Audio Output parameters.
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
			//gpio_set_gpio_pin(UP);
			pdca_load_channel( AVR32_PDCA_CHANNEL_SSC_TX, (void *)&ram_buffer2, 1024);//2048);	// Tx_size);
			//gpio_clr_gpio_pin(UP);
			Tx_buff1 = false;
			Tx_buff2 = true;
			Tx1_Sent = false;
			Tx2_Sent = true;
		} 
		else if (in_buffer && Tx2_Sent)
		{
			//gpio_set_gpio_pin(UP);
			pdca_load_channel( AVR32_PDCA_CHANNEL_SSC_TX, (void *)&ram_buffer1, 1024);//2048);	// Tx_size);
			//gpio_clr_gpio_pin(UP);
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
	gpio_enable_gpio_pin(LED1);
	gpio_clr_gpio_pin(LED1);		// On board LED
	gpio_enable_gpio_pin(LED2);
	gpio_clr_gpio_pin(LED2);		// On board LED
	
	gpio_enable_gpio_pin(Bl_En);	// LCD On/Back light
	gpio_clr_gpio_pin(Bl_En);
	gpio_enable_gpio_pin(Disp_On);
	gpio_clr_gpio_pin(Disp_On);
	
	// INPUTS	-> enable output driver for input pin? ********************? ?
	/*gpio_local_enable_pin_output_driver(UP);
	gpio_local_enable_pin_output_driver(ENTER);
	gpio_local_enable_pin_output_driver(LEFT);
	gpio_local_enable_pin_output_driver(RIGHT);
	gpio_local_enable_pin_output_driver(DOWN);
	gpio_local_enable_pin_output_driver(EXIT);*/
	
	gpio_enable_gpio_pin(UP);
	gpio_set_gpio_pin(UP);
	gpio_enable_gpio_pin(ENTER);	
	gpio_set_gpio_pin(ENTER);
	gpio_enable_gpio_pin(LEFT);	
	gpio_set_gpio_pin(LEFT);
	gpio_enable_gpio_pin(DOWN);	
	gpio_set_gpio_pin(DOWN);
	gpio_enable_gpio_pin(RIGHT);	
	gpio_set_gpio_pin(RIGHT);
	gpio_enable_gpio_pin(EXIT);	
	gpio_set_gpio_pin(EXIT);
	
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
		gpio_tgl_gpio_pin(LED1);
		
		for (b=0; b<25; b++)	// b<25
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
		
		for (b=0; b<25; b++)	// b<25
		{
			wait();
		}
	}	
}
//===================================================
void stop_play(void)
{
	char filename1[30];
	
	// Disable PDCA Transfer (TRANSFER_COMPLETE)
	if (pdca_get_transfer_status(AVR32_PDCA_CHANNEL_SSC_TX) & PDCA_TRANSFER_COMPLETE)
	{
		pdca_disable_interrupt_transfer_complete(AVR32_PDCA_CHANNEL_SSC_TX);
		if (uda1330_output_params.callback_opt & AUDIO_DAC_OUT_OF_SAMPLE_CB)
		  uda1330_output_params.callback(AUDIO_DAC_OUT_OF_SAMPLE_CB);
	}
	
	// Disable PDCA Transfer (RELOAD_IS_ZERO)
	if (pdca_get_transfer_status(AVR32_PDCA_CHANNEL_SSC_TX) & PDCA_TRANSFER_COUNTER_RELOAD_IS_ZERO)
	{
		pdca_disable_interrupt_reload_counter_zero(AVR32_PDCA_CHANNEL_SSC_TX);
		if (uda1330_output_params.callback_opt & AUDIO_DAC_RELOAD_CB)
		  uda1330_output_params.callback(AUDIO_DAC_RELOAD_CB);
	}
	
	// Back to 'Main Menu' or 'Menu' Grid -> then 'Exit' again to get to 'Main Menu'
	im_no = 99;
	Get_Image_file(filename1, im_no);
	Image_Decode(filename1);	
}

//===================================================
//********************* Main ************************
//===================================================
int main (void)
{	
	bool q = 0;			// DOWN
	bool r = 0;			// UP
	bool s = 0;			// RIGHT
	bool t = 0;			// LEFT
 	bool u = 0;			// ENTER
	bool v = 0;			// EXIT
	char filename2[30];
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
	gpio_set_pin_high(LED1);
	
	// initialize SD-SPI and PDCA options
	sd_reader_init();

	im_no = 0;								// Display Intro Screen
	Get_Image_file(filename1, im_no);
	
	gpio_set_pin_low(Bl_En);				// Back light off
	Image_Decode(filename1);
	gpio_set_pin_high(Bl_En);				// Back light on
	
//  	Get_Audio_file(filename2, 0);			// after image -> play Intro audio
//  	Audio_Decode(filename2);
		
	u = true;								// wait for 'ENTER' button press
	while (u != 0)
	{	
		u = gpio_get_pin_value(ENTER);		
	}
	u = true;
	//stop_play();							// Enter -> stop audio -> Main-Menu
	
	// Initial Menu Settings
	im_X	= 0;							// main menu X pos start
	im_Y	= 0;							// main menu Y pos start
	menu	= 0;							// Main Menu (LEARN/TEST)
	im_no	= 98;							// main menu 1
	//Display Main Menu 1
	Get_Image_file(filename1, im_no);
	Image_Decode(filename1);
	
	q = true;								// UP
	r = true;								// DOWN
	s = true;								// LEFT
	t = true;								// RIGHT
	u = true;								// ENTER
	v = true;								// ESCAPE
	
	// state machine -> to continuously loop through program.
		/*switch(X_X)
		{
			case 1:
				pin_check();
				break;
			case 2:
				navigate(^_^);
				break;
			case 3:
				Audio_Decode();
				break;
			default
				pin_check();
				break;
		}	*/		
	
	// Loop through button check
	while(1)
	{
		q = gpio_get_pin_value(DOWN);
		r = gpio_get_pin_value(UP);
		s = gpio_get_pin_value(RIGHT);
		t = gpio_get_pin_value(LEFT);
		u = gpio_get_pin_value(ENTER);
		v = gpio_get_pin_value(EXIT);
		
		if (q == false)						// move image DOWN
		{
			navigate(2);
			s = true;
		}
		else if (r == false)				// move image UP
		{
			navigate(3);
			t = true;
		}
		if (s == false)						// move image RIGHT
		{
			navigate(0);
			s = true;
		}
		else if (t == false)				// move image LEFT
		{
			navigate(1);
			t = true;
		}
		else if (u == false)				// SELECT/ENTER
		{
			navigate(4);
			u = true;
		}
		else if (v == false)				// ESCAPE/EXIT
		{
			navigate(5);
			v = true;
		}	
	}		
}

//===================================================
// ********** Navigate the menus ***************** //
//===================================================
// * im_X and im_Y are X-Y coordinates on the sub-menu
// * Must then be converted into the correct image_no
// * Then converted into Get_Image_file(filename1, im_no);
void navigate(unsigned short keypress)
{
	char filename1[30];
	char filename2[30];
	
	switch (keypress)
	{
	case 0:											//** RIGHT **
		if (menu == 0 && im_no < 99) im_no++;		// 98 -> 99 (Main Menu 1 -> 2)
		
		else if (menu == 1 && im_X < 3) im_X++;		// menu COLUMN[0, 1, 2, 3]
		
		break;
	case 1:											//** LEFT **
		if (menu == 0 && im_no > 98) im_no--;		// 99 -> 98 (Main Menu 1 <- 2)
		
		else if (menu == 1 && im_X > 0) im_X--;		// menu COLUMN[3, 2, 1, 0]
				
		break;
	case 2:											// DOWN
		if (menu == 1 && im_Y < 2) im_Y++;			// menu ROW[0, 1, 2]
		
		break;
	case 3:											// UP
		if (menu == 1 && im_Y > 0) im_Y--;			// menu ROW[2, 1, 0]
		
		break;
	case 4:											// ENTER
		if (menu == 0 && im_no == 98)
		{
			mode	= 0;							// LEARN MODE
			menu	= 1;
			im_no	= 1;
		}
		else if (menu == 0 && im_no == 99)
		{
			mode	= 1;							// TEST MODE
			menu	= 1;
			im_no	= 1;
		}
		// ANSWER MODE
		else if (menu == 1 && mode == 0)
		{
			im_no += 20;							// eg. Answer1 = image 20
			aud_no = im_no;							// [20 - 31]
								
			Get_Image_file(filename1, im_no);		// jump to full images for scrolling
			Image_Decode(filename1);				// display image

			Get_Audio_file(filename2, aud_no);
			Audio_Decode(filename2);				// after image -> play audio
			im_no -= 20;
			check = 1;								// skip redisplaying full image
		}
		// QUESTION MODE
		else if (menu == 1 && mode == 1)
		{
			im_no += 40;							// eg. Question1 = image 40
			aud_no = im_no;							// [40 -> 51]
			
			Get_Image_file(filename1, im_no);
			Image_Decode(filename1);				// display image
			
			Get_Audio_file(filename2, aud_no);
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
		if (menu != 0)									// => MENU NAVIGATION
		{
			// convert X-Y into correct image number
			switch(im_X)								// column
			{
				case 0:
					if(im_Y == 0) im_no = 1;			// Row
					else if(im_Y == 1) im_no = 5;
					else if(im_Y == 2) im_no = 9;
					break;
				case 1:
					if(im_Y == 0) im_no = 2;			// Row
					else if(im_Y == 1) im_no = 6;
					else if(im_Y == 2) im_no = 10;
					break;
				case 2:
					if(im_Y == 0) im_no = 3;			// Row
					else if(im_Y == 1) im_no = 7;
					else if(im_Y == 2) im_no = 11;
					break;
				case 3:
					if(im_Y == 0) im_no = 4;			// Row
					else if(im_Y == 1) im_no = 8;
					else if(im_Y == 2) im_no = 12;
					break;
			}
		}			
		
		Get_Image_file(filename1, im_no);
		Image_Decode(filename1);
	}		
	check = 0;
}

//===================================================
// ********** FAT GET FILENAME ******************* //
//===================================================
void Get_Image_file(char * buf, int choice)
 {
	unsigned char i_str = 3;		// unsigned long i_str = 3;
	unsigned short file;
	unsigned short k = 0;
	
	unsigned char folder[23];
	unsigned char Intro[22]		= "A:/Folder1\\File00.bmp";
	unsigned char M_Menu1[22]	= "A:/Folder1\\File01.bmp";
	unsigned char M_Menu2[22]	= "A:/Folder1\\File02.bmp";
	
	unsigned char Menu1[22]		= "A:/Folder1\\File03.bmp";
	unsigned char Menu2[22]		= "A:/Folder1\\File04.bmp";
	unsigned char Menu3[22]		= "A:/Folder1\\File05.bmp";
	unsigned char Menu4[22]		= "A:/Folder1\\File06.bmp";
	unsigned char Menu5[22]		= "A:/Folder1\\File07.bmp";
	unsigned char Menu6[22]		= "A:/Folder1\\File08.bmp";
	unsigned char Menu7[22]		= "A:/Folder1\\File09.bmp";
	unsigned char Menu8[22]		= "A:/Folder1\\File10.bmp";
	unsigned char Menu9[22]		= "A:/Folder1\\File11.bmp";
	unsigned char Menu10[22]	= "A:/Folder1\\File12.bmp";
	unsigned char Menu11[22]	= "A:/Folder1\\File13.bmp";
	unsigned char Menu12[22]	= "A:/Folder1\\File14.bmp";
	
	unsigned char Ans1[22]		= "A:/Folder1\\File15.bmp";
	unsigned char Ans2[22]		= "A:/Folder1\\File16.bmp";
	unsigned char Ans3[22]		= "A:/Folder1\\File17.bmp";
	unsigned char Ans4[22]		= "A:/Folder1\\File18.bmp";
	/*unsigned char Ans5[22]		= "A:/Folder1\\File19.bmp";
	unsigned char Ans6[22]		= "A:/Folder1\\File120.bmp";
	unsigned char Ans7[22]		= "A:/Folder1\\File21.bmp";
	unsigned char Ans8[22]		= "A:/Folder1\\File22.bmp";
	unsigned char Ans9[22]		= "A:/Folder1\\File23.bmp";
	unsigned char Ans10[22]		= "A:/Folder1\\File24.bmp";
	unsigned char Ans11[22]		= "A:/Folder1\\File25.bmp";*/
	unsigned char Ans12[22]		= "A:/Folder1\\File26.bmp";
	
	unsigned char Quest1[22]	= "A:/Folder1\\File27.bmp";
	unsigned char Quest2[22]	= "A:/Folder1\\File28.bmp";
	unsigned char Quest3[22]	= "A:/Folder1\\File29.bmp";
	/*unsigned char Quest1[22]	= "A:/Folder1\\File27.bmp";
	unsigned char Quest2[22]	= "A:/Folder1\\File28.bmp";
	unsigned char Quest3[22]	= "A:/Folder1\\File29.bmp";
	unsigned char Quest1[22]	= "A:/Folder1\\File27.bmp";
	unsigned char Quest2[22]	= "A:/Folder1\\File28.bmp";
	unsigned char Quest3[22]	= "A:/Folder1\\File29.bmp";
	unsigned char Quest1[22]	= "A:/Folder1\\File27.bmp";
	unsigned char Quest2[22]	= "A:/Folder1\\File28.bmp";
	unsigned char Quest3[22]	= "A:/Folder1\\File29.bmp";*/
	
	switch (choice)
	{
	case 0:									// START SCREEN
		while (k<22)
		{
			folder[k] = Intro[k];
			k++;
		}
		break;
	case 1:									// Menu grid Image 1
		while (k<22)
		{
			folder[k] = Menu1[k];
			k++;
		}
		break;
	case 2:									// Menu grid Image 2
		while (k<22)
		{
			folder[k] = Menu2[k];
			k++;
		}
		break;
	case 3:									// Menu grid Image 3
		while (k<22)
		{
			folder[k] = Menu3[k];
			k++;
		}
		break;
	case 4:									// Menu grid Image 4
		while (k<22)
		{
			folder[k] = Menu4[k];
			k++;
		}
		break;
	case 5:									// Menu grid Image 5
		while (k<22)
		{
			folder[k] = Menu5[k];
			k++;
		}
		break;
	case 6:									// Menu grid Image 6
		while (k<22)
		{
			folder[k] = Menu6[k];
			k++;
		}
		break;
	case 7:									// Menu grid Image 7
		while (k<22)
		{
			folder[k] = Menu7[k];
			k++;
		}
		break;
	case 8:									// Menu grid Image 8
		while (k<22)
		{
			folder[k] = Menu8[k];
			k++;
		}
		break;
	case 9:									// Menu grid Image 9
		while (k<22)
		{
			folder[k] = Menu9[k];
			k++;
		}
		break;
	case 10:								// Menu grid Image 10
		while (k<22)
		{
			folder[k] = Menu10[k];
			k++;
		}
		break;
	case 11:								// Menu grid Image 11
		while (k<22)
		{
			folder[k] = Menu11[k];
			k++;
		}
		break;
	case 12:								// Menu grid Image 11
		while (k<22)
		{
			folder[k] = Menu12[k];
			k++;
		}
		break;
	
	case 20:								// Answer Image 1
		while (k<22)
		{
			folder[k] = Ans1[k];
			k++;
		}
		break;
	case 21:								// Answer Image 2
		while (k<22)
		{
			folder[k] = Ans2[k];
			k++;
		}
		break;
	case 22:								// Answer Image 3
		while (k<22)
		{
			folder[k] = Ans3[k];
			k++;
		}
		break;
	case 23:								// Answer Image 4
		while (k<22)
		{
			folder[k] = Ans4[k];
			k++;
		}
		break;
	case 31:								// Answer Image 12
		while (k<22)
		{
			folder[k] = Ans12[k];
			k++;
		}
		break;
	case 40:								// Question Image 1
		while (k<22)
		{
			folder[k] = Quest1[k];
			k++;
		}
		break;
	case 41:								// Question Image 2
		while (k<22)
		{
			folder[k] = Quest2[k];
			k++;
		}
		break;
	case 42:								// Question Image 3
		while (k<22)
		{
			folder[k] = Quest3[k];
			k++;
		} 
		break;
	case 98:								// Main Menu 1
		while (k<22)
		{
			folder[k] = M_Menu1[k];
			k++;
		}
		break;
	case 99:								// Main Menu 2
		while (k<22)
		{
			folder[k] = M_Menu2[k];
			k++;
		}
		break;
	default:								// Intro Screen as default
		while (k<22)
		{
			folder[k] = Intro[k];
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
		
		if (i_str == 22)							// text file
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
	
	// ssc_i2s_init(ssc, 44100, 16, 16, SSC_I2S_MODE_STEREO_OUT, FPBA_HZ);
	unsigned char folder1[23];
	unsigned char IntroAu[22] = "A:/Folder2\\LOUDER.raw";		// Intro Track
	unsigned char Audio0[22] = "A:/Folder2\\File00.raw";		// NoDeliveryVehicles
	unsigned char Audio1[22] = "A:/Folder2\\File01.raw";		// NoDeliveryVehicles + QT
	unsigned char Audio2[22] = "A:/Folder2\\File02.raw";		// ParkingForConstructionVehicles
	unsigned char Audio3[22] = "A:/Folder2\\File03.raw";		// ParkingForConstructionVehicles + QT
	unsigned char Audio4[22] = "A:/Folder2\\File04.raw";		// TollRoad
	unsigned char Audio5[22] = "A:/Folder2\\File05.raw";		// TollRoad + QT
	unsigned char Audio6[22] = "A:/Folder2\\File06.raw";		// ParkingMidiBus
	unsigned char Audio7[22] = "A:/Folder2\\File07.raw";		// ParkingMidiBus + QT
	unsigned char Audio8[22] = "A:/Folder2\\File08.raw";		// NoLoudNoise
	unsigned char Audio9[22] = "A:/Folder2\\File09.raw";		// NoLoudNoise + QT
	unsigned char Audio10[22] = "A:/Folder2\\File10.raw";		// FreewayBegins
	unsigned char Audio11[22] = "A:/Folder2\\File11.raw";		// FreewayBegins + QT
	unsigned char Audio12[22] = "A:/Folder2\\File12.raw";		// MinimumSpeed
	unsigned char Audio13[22] = "A:/Folder2\\File13.raw";		// MinimumSpeed + QT
	unsigned char Audio14[22] = "A:/Folder2\\File14.raw";		// NoAbnormalVehicles
	unsigned char Audio15[22] = "A:/Folder2\\File15.raw";		// NoAbnormalVehicles + QT
	
	file = false;
 	buf[0] = 'A';
 	buf[1] = ':';
 	buf[2] = '/';
	
	switch(choice)
	{
		case 0:	while (k<22)					// File1.raw (Intro Track)
					{
						folder1[k] = IntroAu[k];
						k++;
					}
					break;
		case 21:	while (k<22)					// File00.raw (Learn)
					{
						folder1[k] = Audio0[k];
						k++;
					}
					break;
		case 41:	while (k<22)					// File01.raw (Test)
					{
						folder1[k] = Audio1[k];
						k++;
					}
					break;
		case 22:	while (k<22)					// File02.raw (Learn)
					{
						folder1[k] = Audio2[k];
						k++;
					}
					break;
		case 42:	while (k<22)					// File03.raw (Test)
					{
						folder1[k] = Audio3[k];
						k++;
					}
					break;
		case 23:	while (k<22)					// File04.raw (Learn)
					{
						folder1[k] = Audio4[k];
						k++;
					}
					break;
		case 43:	while (k<22)					// File05.raw (Test)
					{
						folder1[k] = Audio5[k];
						k++;
					}
					break;
		case 24:	while (k<22)					// File06.raw (Learn)
					{
						folder1[k] = Audio6[k];
						k++;
					}
					break;
		case 44:	while (k<22)					// File07.raw (Test)
					{
						folder1[k] = Audio7[k];
						k++;
					}
					break;
		case 25:	while (k<22)					// File08.raw (Learn)
					{
						folder1[k] = Audio8[k];
						k++;
					}
					break;
		case 45:	while (k<22)					// File09.raw  (Test)
					{
						folder1[k] = Audio9[k];
						k++;
					}
					break;
		case 26:	while (k<22)					// File10.raw (Learn)
					{
						folder1[k] = Audio10[k];
						k++;
					}
					break;
		case 46:	while (k<22)					// File11.raw (Test)
					{
						folder1[k] = Audio11[k];
						k++;
					}
					break;
		case 27:	while (k<22)					// File12.raw (Learn)
					{
						folder1[k] = Audio12[k];
						k++;
					}
					break;
		case 47:	while (k<22)					// File12.raw (Test)
					{
						folder1[k] = Audio13[k];
						k++;
					}
					break;
		case 28:	while (k<22)					// File12.raw (Learn)
					{
						folder1[k] = Audio14[k];
						k++;
					}
					break;
		default:	while (k<22)					// LOUDER.raw (intro)
					{
						folder1[k] = IntroAu[k];
						k++;
					}
					break;	
	}
	
	while (file == false)
	{	
		buf[i_str] = folder1[i_str];				// set buf to file name from [3]
		i_str++;
		
		if (i_str == 22)							// text file
		{
			// Add NUL character
			buf[i_str] = '\0';
			file = true;
		}
	}
 }
 
//===================================================
// ********** FAT Open File ********************** //
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
			if (esc == false)					// move image 
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