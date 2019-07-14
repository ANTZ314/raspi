/* 
 * File:   main.h
 * Author: SmithAD
 *
 * Created on October 7, 2015, 9:34 PM
 */

#ifndef MAIN_H
#define	MAIN_H

#ifdef	__cplusplus
extern "C" {
#endif

    #ifndef _XTAL_FREQ
    #define _XTAL_FREQ    4000000     // 8Mhz INTOSC internal osc
    #define __delay_us(x) _delay((unsigned long)((x)*(_XTAL_FREQ/4000000.0)))
    //#define __delay_ms(x) _delay((unsigned long)((x)*(_XTAL_FREQ/4000.0)))
    #endif

    unsigned int PA_Nibble  = 0x00;

    #define high            1
    #define low             0

    #define LCDlen          17

    #define RS              RB0         // LCD Read Select ?
    #define RS_ON           RB0 = 1     // output_high(RB0)         //PIN_B0)		// LCD Register Select (HIGH)
    #define RS_OFF          RB0 = 0     // output_low(RB0)          //PIN_B0)		// LCD Register Select (LOW)
    #define ENABLE          RA4         // LCD Enable

//  #define RS_ON           RB3 = 1     // RS-485 chip select
//  #define RS_OFF          RB3 = 0     // RS-485 chip deselect
    
    #define status          RB4         // PIN_B4                   // LED status light
    #define LED_ON          RB4 = 0     // output_low(RB4)
    #define LED_OFF         RB4 = 1     // output_high(RB4)

    #define Rx_PIC          RB2         // PIN_B2                   // RS485 Direction Enable (0 - Recieve / 1 - Transmit)
    #define Tx_PIC          RB5         // PIN_B5                   // RS485 Data line  (A normally HIGH)
    #define RS_Sel          RB3         // PIN_B3                   // RS485 Clock line (B normally LOW)

    #define PB_1            RA6         // PIN_B6
    #define PB_2            RA7         // PIN_B7

    /* LCD GENERAL PIN DEFINES (4bit mode) */
    #define D4              RA0         // LCD Data pin 4
    #define D5              RA1         // LCD Data pin 5
    #define D6              RA2         // LCD Data pin 6
    #define D7              RA3         // LCD Data pin 7

    #define EN              (PA_Nibble &  0x10)         // Just E On
    #define EN_ON           (PA_Nibble |= 0x10)         // Enable High
    #define EN_OFF          (PA_Nibble &= ~0x10)        // Enable Low
    #define LCD4            (PA_Nibble &  0x01)         // Just LCD4 On
    #define LCD4_ON         (PA_Nibble |= 0x01)
    #define LCD4_OFF        (PA_Nibble &= ~0x01)
    #define LCD5            (PA_Nibble &  0x02)         // Just LCD5 On
    #define LCD5_ON         (PA_Nibble |= 0x02)
    #define LCD5_OFF        (PA_Nibble &= ~0x02)
    #define LCD6            (PA_Nibble &  0x04)         // Just LCD6 On
    #define LCD6_ON         (PA_Nibble |= 0x04)
    #define LCD6_OFF        (PA_Nibble &= ~0x04)
    #define LCD7            (PA_Nibble &  0x08)         // Just LCD7 On
    #define LCD7_ON         (PA_Nibble |= 0x08)
    #define LCD7_OFF        (PA_Nibble &= ~0x08)

#ifdef	__cplusplus
}
#endif

#endif	/* MAIN_H */

