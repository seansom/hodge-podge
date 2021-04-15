/*
 * main.c
 * Sample code for using the Capture-Compare-PWM peripheral of
 * PIC32MM0xx-series chips
 * 
 * EEE 158: Electrical and Electronics Engineering Laboratory V
 * 
 * Electrical and Electronics Engineering Institute, College of Engineering
 * University of the Philippines - Diliman
 */

#include <xc.h>
#include <stdint.h>

/*
 * Program-wide variables are declared here. With embedded systems,
 * uninitialized variables are a big no-no!
 * 
 * A limitation of the MPLAB X IDE is the inability to directly modify SFRs
 * during runtime. We instead modify variables that get shadowed into the SFRs
 * within the infinite loop.
 */
int16_t pwm_ra = 0;     // Activate at the start of every period
int16_t pwm_rb = 450;   // Deactivate at this time within the period

int main(void)
{ 
    /*
     * BEGIN PWM setup
     * 
     * For microcontrollers, PWM is often a part of a more-general module
     * called input/output capture/compare, which often has PWM as an option;
     * shorthand is CCP.
     * 
     * The PIC32MMxxxx CCP can operate in one of several modes, as provided in
     * the family datasheet. PWM is under Output Compare mode, since the core
     * idea of PWM is to produce pulses whose width is some fraction of the
     * period.
     */
    
    /*
     * Unlike ADC, where ON must be set prior to setting other bits; in PWM
     * the modes must be setup *prior* to enabling the module.
     */
    CCP1CON1bits.T32    = 0b0;      // 16-bit; PWM is not available in 32-bit
    CCP1CON1bits.CCSEL  = 0b0;      // Output Compare/PWM mode
    CCP1CON1bits.MOD    = 0b0101;   // PWM mode
    
    CCP1CON2bits.OCAEN  = 1;        // Enable Output A (ie. OC1A)
    
    CCP1CON3bits.POLACE = 0;        // Active ('ON') state is HIGH
    CCP1CON3bits.PSSACE = 0b10;     // Force-OFF the output when the PWM is shutdown
    
    /*
     * CCPxPR specifies the PWM period according to the formula
     * 
     * t_{PWM,x} = CCPxPR / f_{CCPx}
     * 
     * where f_{CCPx} is the PWM clock for CCP module x, as determined by its
     * CLKSEL and TMRPS bits.
     */
    CCP1CON1bits.CLKSEL = 0b000;   // Input clock = system clock (fosc)
    CCP1CON1bits.TMRPS  = 0b00;    // Actual PWM clock = (input clk)/1
    CCP1PR              = 700;     // Period = 1000/(actual PWM clock)
    CCP1RA              = pwm_ra;  // RA and RB set the ON-times...    
    CCP1RB              = pwm_rb;  // ... see note at the top of this file
    
    /// END PWM setup
    
    /*
     * BEGIN Port setup
     * 
     * PWM is one of so-called "alternate functions". Its associated pin must
     * be properly configured as well; this time, the device-specific datasheet
     * will need to be consulted in addition to the family datasheet to figure
     * out which PORT register set to use.
     */
    
    // OC1A is tied to PORT B, Channel 8.
    TRISBbits.TRISB8 = 0;       // Output
    ANSELBbits.ANSB0 = 0;       // Digital mode
    
    /// END Port setup
    
    ////////////////////////////////////////////////////////////////////////
    
    /*
     * As always, microcontroller main()s are not supposed to return to the
     * caller.
     */
    CCP1CON1bits.ON = 1;    // Enable PWM
    for (;;) {
        /*
         * As the PWM is a hardware resource, it continues to run independent
         * of the CPU. Because it is double-buffered per the family datasheet,
         * it is possible to update the duty cycle and period without turning
         * OFF the PWM first (although it is usually the duty cycle only that
         * is modified during runtime).
         */
        CCP1RA = pwm_ra;
        CCP1RB = pwm_rb;
        
        asm volatile("nop");
        asm volatile("nop");
        asm volatile("nop");
    }
    return 1;
}