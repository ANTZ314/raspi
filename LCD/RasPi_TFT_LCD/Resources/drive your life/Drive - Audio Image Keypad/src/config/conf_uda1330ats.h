#ifndef CONF_UDA1330ATS_H_
#define CONF_UDA1330ATS_H_

#include "flashc.h"
#include "pm.h"
#include "gpio.h"

//==========================================================================
//																  Prototypes 
//==========================================================================
void init_sys_clocks(void);
void init_dac_gclk(void);
bool uda1330_dac_output(void *sample_buffer, size_t sample_length);

//==========================================================================
//											Control words for UDA1330ATS DAC 
//==========================================================================
#define UDA1330_GCLK_ID             0
#define UDA1330_GCLK_PIN            AVR32_PM_GCLK_0_1_PIN			// -> PB19 [GPIO 51]
#define UDA1330_GCLK_FUNCTION       AVR32_PM_GCLK_0_1_FUNCTION

// from "conf_audio_player.h"
// from init_sys_clocks() -> PLL0 output = 62.0928 MHz
#define FMCK_HZ                           62092800
#define FCPU_HZ                           FMCK_HZ
#define FHSB_HZ                           FCPU_HZ
#define FPBB_HZ                           FMCK_HZ
#define FPBA_HZ                           FMCK_HZ


//! Default heap initialization word.
#define DEFAULT_HEAP_INIT_WORD            0xA5A5A5A5				// 32 bit value

//==========================================================================
//															    From audio.h 
//==========================================================================
#define AUDIO_DAC_OUT_OF_SAMPLE_CB     1       //!< Out of sample callback for the output
#define AUDIO_DAC_RELOAD_CB            2       //!< Reload callback for the output
#define AUDIO_ADC_OUT_OF_SAMPLE_CB     4       //!< Out of sample callback for the input
#define AUDIO_ADC_RELOAD_CB            8       //!< Reload callback for the input


//#define SD_MMC_INCLUDED                   true			// conf_access.h [line 74]

// from "clocks_fosc0_12000000_fosc1_11289600.c"
/*
	OSC 0 -> 12.0000 MHz	-> Nothing
	PLL 1 -> 48.0000 MHz	-> Nothing
	OSC 1 -> 11.2896 MHz	-> Gen Clock
	PLL 0 -> 62.0928 MHz	-> PBA
*/
void init_sys_clocks(void)
{
	volatile avr32_pm_t* pm = &AVR32_PM;
	
	// Switch to OSC0 to speed up the booting
	pm_switch_to_osc0(pm, FOSC0, OSC0_STARTUP);
	
	pm_enable_osc1_crystal(pm, FOSC1);
	pm_enable_clk1(pm, OSC1_STARTUP);

//===============================================================================
	  // Set PLL0 (fed from OSC1 = 11.2896 MHz) to 124.1856 MHz
	  // We use OSC1 since we need a correct master clock for the SSC module to 
	  // generate the correct sample rate -> 62.0928 MHz
//===============================================================================
	  pm_pll_setup(pm, 
					0,										// pll. (0 for PLL0, 1 for PLL1)
					10,										// mul.	(11.2896MHz x 11)
					1,										// div. (DIV=1)
					1,										// osc. (0 for osc0, 1 for osc1)
					16);									// lockcount.

	  // Set PLL operating range and divider (fpll = fvco/2)
	  // -> PLL0 output = 62.0928 MHz
	  pm_pll_set_option(pm, 
						0,									// (0 for PLL0, 1 for PLL1)
						1,									// pll_freq. VCO Freq range 80-180MHz
						1,									// pll_div2.	
						0);									// pll_wbwdisable. [0 = enable wide bandwidth mode]

	  // start PLL0 and wait for the lock
	  pm_pll_enable(pm, 0);									// PPL0 62.0928MHz
	  pm_wait_for_pll0_locked(pm);							// 
  
	  // Set all peripheral clocks to run at master clock rate (PLL0)
	  pm_cksel(pm,
				0,											// pbadiv. -> devide by 2?
				1,											// pbasel.	-> was selected -> 62.0928 MHz
				0,											// pbbdiv.	-> 0 = disable
				0,											// pbbsel.
				0,											// hsbdiv.
				0);											// hsbsel.

	  // Set one wait state for the flash
	  flashc_set_wait_state(1);								// flash controller not used/included

	  // Switch to PLL0 as the master clock
	  pm_switch_to_clock(pm, AVR32_PM_MCCTRL_MCSEL_PLL0);	// -> 62.0928MHz on PBA (SSC from there)
	  
//===============================================================================
	// Use 12MHz from OSC0 and generate 96 MHz on PLL1
//===============================================================================
	pm_pll_setup(&AVR32_PM, 
				 1,  				// pll1
				 7,   				// mul.
				 1,   				// div.
				 0,   				// osc.
				 16); 				// lockcount.

	// Div 96MHz by 2 -> PLL1 = 48MHz
	pm_pll_set_option(&AVR32_PM, 
				1,					// pll1
				1,					// pll_freq: choose the range 80-180MHz.
				1,					// pll_div2 -> 96MHz/2 = 48MHz
				0);					// pll_wbwdisable.

	// start PLL1 and wait forl lock
	pm_pll_enable(&AVR32_PM, 1);

	// Wait for PLL1 locked.
	pm_wait_for_pll1_locked(&AVR32_PM);			// PLL1 = 48MHz 


	//init_dac_gclk();
}

// Directly output Osc1 (11.2896MHz) onto generic clk pin for DAC: SYSTEM CLOCK (pin 6)
void init_dac_gclk(void)
{
	volatile avr32_pm_t* pm = &AVR32_PM;
  
	/* start oscillator1 */
	pm_enable_osc1_crystal(pm, FOSC1);
	pm_enable_clk1(pm, OSC1_STARTUP);
  
	// original 11.2896MHz Generic Clock		  
	pm_gc_setup(pm,
		  UDA1330_GCLK_ID,		// which generic clk (GClk0)
		  0,					// Use Osc (=0) or PLL (=1), here PLL
		  1,					// Select Osc0/PLL0 or Osc1/PLL1
		  0,					// disable divisor
		  0);					// no divisor => 11.2896MHz

	/* Enable Generic clock */
	pm_gc_enable(pm, UDA1330_GCLK_ID);
    //pm_gc_disable(pm, UDA1330_GCLK_ID);			// stop perminent running 11.2MHz GClk
	
	/* Set the GCLOCK function to the GPIO pin */
	gpio_enable_module_pin(UDA1330_GCLK_PIN, UDA1330_GCLK_FUNCTION);
	
}

#endif /* CONF_UDA1330ATS_H_ */

