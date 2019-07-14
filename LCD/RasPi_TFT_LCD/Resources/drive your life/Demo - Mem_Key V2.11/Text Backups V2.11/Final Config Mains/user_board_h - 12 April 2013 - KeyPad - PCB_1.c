#ifndef USER_BOARD_H
#define USER_BOARD_H

#include "compiler.h"

//==========================================================================
//														Oscillator set up
//==========================================================================
#define FOSC32          32768                                 //!< Osc32 frequency: Hz.
#define OSC32_STARTUP   AVR32_PM_OSCCTRL32_STARTUP_8192_RCOSC //!< Osc32 startup time: RCOsc periods.

#define FOSC0           12000000                              //!< Osc0 frequency: Hz.
#define OSC0_STARTUP    AVR32_PM_OSCCTRL0_STARTUP_2048_RCOSC  //!< Osc0 startup time: RCOsc periods.

#define FOSC1           11289600                              //!< Osc0 frequency: Hz.
#define OSC1_STARTUP    AVR32_PM_OSCCTRL0_STARTUP_2048_RCOSC  //!< Osc0 startup time: RCOsc periods.

// These are documented in services/basic/clock/uc3b0_b1/osc.h
#define BOARD_OSC0_HZ				12000000
#define BOARD_OSC0_STARTUP_US		17000
#define BOARD_OSC0_IS_XTAL			true

#define BOARD_OSC1_HZ				11289600
#define BOARD_OSC1_STARTUP_US		17000
#define BOARD_OSC1_IS_XTAL			true

#define BOARD_OSC32_HZ				32768
#define BOARD_OSC32_STARTUP_US		71000
#define BOARD_OSC32_IS_XTAL			false

// Power Pin
#define on_off						AVR32_PIN_PA11

//==========================================================================
//										SD_Card Connector / FAT file system
//==========================================================================

//#define SD_MMC_WRITE_PROTECT_PIN    AVR32_PIN_PB01				// column 2 keypad
//#define SD_MMC_CARD_DETECT_PIN      AVR32_PIN_PA06				// column 1 keypad
#define SD_MMC_SPI                  (&AVR32_SPI0)					// (&AVR32_SPI1)
#define SD_MMC_SPI_NPCS             0
#define SD_MMC_SPI_SCK_PIN          AVR32_SPI0_SCK_0_0_PIN
#define SD_MMC_SPI_SCK_FUNCTION     AVR32_SPI0_SCK_0_0_FUNCTION
#define SD_MMC_SPI_MISO_PIN         AVR32_SPI0_MISO_0_0_PIN
#define SD_MMC_SPI_MISO_FUNCTION    AVR32_SPI0_MISO_0_0_FUNCTION
#define SD_MMC_SPI_MOSI_PIN         AVR32_SPI0_MOSI_0_0_PIN
#define SD_MMC_SPI_MOSI_FUNCTION    AVR32_SPI0_MOSI_0_0_FUNCTION
#define SD_MMC_SPI_NPCS_PIN         AVR32_SPI0_NPCS_0_0_PIN			// AVR32_SPI_NPCS_0_0_PIN => PA16
#define SD_MMC_SPI_NPCS_FUNCTION    AVR32_SPI0_NPCS_0_0_FUNCTION

#define NB_SECTOR_TO_SEND    4

//==========================================================================
//												  Receive -> PDCA SPI Module 
//==========================================================================
#define UDA1330_SPI                         (&AVR32_SPI0)			
#define UDA1330_SPI_RX_PDCA_PID             AVR32_PDCA_PID_SPI0_RX	// defined as '
#define UDA1330_SPI_RX_PDCA_CHANNEL         0						// Same channel ? ?
#define UDA1330_SPI_RX_PDCA_IRQ             AVR32_PDCA_IRQ_0		// PDCA interrupt
#define UDA1330_SPI_RX_PDCA_INT_LEVEL       0						// highest priority

//#define UDA1330_SPI_TX_PDCA_PID			AVR32_PDCA_PID_SPI0_TX 
//#define UDA1330_SPI_TX_PDCA_CHANNEL		1						// In the example we will use the pdca channel 1.

#define UDA1330_SPI_TX_PDCA_PID				AVR32_PDCA_PID_SPI0_TX
#define UDA1330_SPI_TX_PDCA_CHANNEL			1

//==========================================================================
// 												 Transmit -> PDCA SSC Module 
//==========================================================================
#define UDA1330_SSC_TX_PDCA_PID             AVR32_PDCA_PID_SSC_TX	// defined as '9'
#define UDA1330_SSC_TX_PDCA_CHANNEL         2						// Channel match IRQ number ?
#define UDA1330_SSC_TX_PDCA_IRQ             AVR32_PDCA_IRQ_1		// PDCA interrupt
#define UDA1330_SSC_TX_PDCA_INT_LEVEL       1						// priority level equal ?

//#define UDA1330_SPI_RX_PDCA_CHANNEL2      3						// Channel match IRQ number ?
//#define UDA1330_SSC_TX_PDCA_CHANNEL2      2						// Channel match IRQ number ?

//==========================================================================
//															SSC I2S Module 
//==========================================================================
//! \name TI TLV320AIC23B sound chip -> UDA1330ATS
#define SSC							  (&AVR32_SSC)
#define SSC_TX_CLOCK_PIN              AVR32_SSC_TX_CLOCK_0_PIN				// PA15
#define SSC_TX_CLOCK_FUNCTION         AVR32_SSC_TX_CLOCK_0_FUNCTION
#define SSC_TX_DATA_PIN               AVR32_SSC_TX_DATA_0_PIN				// PA16
#define SSC_TX_DATA_FUNCTION          AVR32_SSC_TX_DATA_0_FUNCTION
#define SSC_TX_FRAME_SYNC_PIN         AVR32_SSC_TX_FRAME_SYNC_0_PIN			// PA14
#define SSC_TX_FRAME_SYNC_FUNCTION    AVR32_SSC_TX_FRAME_SYNC_0_FUNCTION

//==========================================================================
//								Was TWI DAC Control Pins -> Static pin mode
//==========================================================================
//#define L3_MODE				AVR32_PIN_PB12			// TWI Mode Control (in L3 Mode)
//#define APPL0					AVR32_PIN_PB12			// (LOW = ON) - (HIGH = MUTED) [Perm. GND]
//#define APPSEL				AVR32_PIN_PB11			// L3_Select-> Vddd = Static Pin Mode
#define APPL1					AVR32_PIN_PA30			// L3_TWCK	-> DEEM = 
#define APPL2					AVR32_PIN_PB12			// L3_Mode	-> SF0  = 0 (I2S)
#define APPL3					AVR32_PIN_PA29			// L3_Data	-> SF1  = 0 (I2S)

//==========================================================================
//													General Test purposes
//==========================================================================
#define LED1					AVR32_PIN_PA09			// Status 1
#define LED2					AVR32_PIN_PA08			// Status 2

// New Board layout defines //
/*#define COL1					AVR32_PIN_PA00			// COL 1
#define COL2					AVR32_PIN_PA01			// COL 2
#define COL3					AVR32_PIN_PA02			// RIGHT

#define ROW1					AVR32_PIN_PA04			// DOWN
#define	ROW2					AVR32_PIN_PA05			// LEFT
#define ROW3					AVR32_PIN_PA06			// ENTER
#define ROW4					AVR32_PIN_PA07			// UP*/

// Old Test Board 2 //
#define COL1					AVR32_PIN_PA00			// COL 1
#define COL2					AVR32_PIN_PA01			// COL 2
#define COL3					AVR32_PIN_PA02			// RIGHT

#define ROW1					AVR32_PIN_PA03			// 
#define	ROW2					AVR32_PIN_PA04			// 
#define ROW3					AVR32_PIN_PA05			// 
#define ROW4					AVR32_PIN_PA06

//============================================================================ 
//														LCD Pin Declarations 
//============================================================================
#define IC_RD					AVR32_PIN_PA23		// Data Enable H-->L
#define IC_WR					AVR32_PIN_PA22		// L: Write, H: Read
#define IC_A0					AVR32_PIN_PA21		// RS: L:Command,H:Data
#define IC_CS					AVR32_PIN_PB04		// L: Chip select
#define Disp_On					AVR32_PIN_PB06		// Display On/Off
#define IC_RST					AVR32_PIN_PB05		// L: RESET
#define Bl_En					AVR32_PIN_PA20		// Back Light -> PWM
//#define IC_UD					AVR32_PIN_P			// L: UP to Down , H: Down to UP
//#define IC_LR					AVR32_PIN_P			// L: Left to Right , H: Right to Left

//============================================================================
//													Define the LCD data bus
//============================================================================
#define LCD0					AVR32_PIN_PA24
#define LCD1					AVR32_PIN_PA25
#define LCD2					AVR32_PIN_PA26
#define LCD3					AVR32_PIN_PA27
#define LCD4					AVR32_PIN_PA28
#define LCD5					AVR32_PIN_PB00
#define LCD6					AVR32_PIN_PB01
#define LCD7					AVR32_PIN_PB02
	
//=============================================================================

#endif // USER_BOARD_H
