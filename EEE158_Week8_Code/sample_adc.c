/*
 * main.c
 * Sample code for using the ADC peripheral of PIC32MM0xx-series chips
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
 */
int16_t adc_value = 0;      // Raw value from the ADC
int16_t pwm_ref = 0;        // Reference for the PWM module

int main(void)
{ 
    /*
     * BEGIN ADC setup
     * 
     * The 'FORM' and 'MODE12' members need special attention, as they directly
     * influence how the read ADC value is represented in memory.
     * 
     * The PIC32MMxxxx ADC can operate in either 10-bit mode, or 12-bit mode;
     * higher resolution is better, but may be precluded by RAM issues (it
     * should not be for this family, since the minimum supported
     * representation of 16 bits is larger than the maximum resolution of 12
     * bits). Since our inputs will never be negative (due to electrical
     * ratings being violated), we select the 16-bit *unsigned* integer form to
     * save on space.
     */
    AD1CON1bits.ON = 1;     // Enable ADC
    AD1CON1bits.FORM = 0;   // See family reference datasheet
    AD1CON1bits.MODE12 = 1; // See family reference datasheet
    AD1CON1bits.ASAM = 0;   // Do NOT auto-sample
    AD1CON1bits.SSRC = 0;   // Clearing SAMP will initiate conversion
    
    AD1CON2bits.VCFG = 0;   // Reference voltage is the power supply (~3.3V)
    AD1CON2bits.CSCNA = 0;  // Only one channel is used, or manual scanning is to be done
    
    /*
     * Select AN3 as (+) input, and Vss (= 0V) as (-) input to ADC
     * 
     * This has the effect of the ADC input being
     * 
     * IN = AN3 - 0 = AN3
     */
    AD1CHSbits.CH0NA = 0b000;       // Selects AVSS (essentially, ground)
    AD1CHSbits.CH0SA = 0b00011;     // Selects AN3
    
    /// END ADC setup
    
    /*
     * BEGIN Port setup
     * 
     * ADC is one of so-called "alternate functions". Its associated pin must
     * be properly configured as well; this time, the device-specific datasheet
     * will need to be consulted in addition to the family datasheet to figure
     * out which PORT register set to use.
     */
    
    // AN3 is tied to PORT B, Channel 1.
    TRISBbits.TRISB1 = 1;
    ANSELBbits.ANSB1 = 1;
    
    /// END Port setup
    
    ////////////////////////////////////////////////////////////////////////
    
    /*
     * As always, microcontroller main()s are not supposed to return to the
     * caller.
     */
    AD1CON1bits.SAMP = 1;
    for (;;) {
        
        /*
         * ADC conversion is initiated using the following steps:
         *  - Set SAMP in AD1CON1
         *  - Wait for at least 3*t_{ad}
         *  - Clear SAMP
         * 
         * When the conversion is complete, DONE in AD1CON1 is set. Since we
         * selected manual sampling and conversion, the most-recent result is
         * always in ADC1BUF0.
         */
        
        if (AD1CON1bits.DONE) {
            /*
             * Conversion complete. Store the buffer's contents into our
             * variable now because as soon as sampling is (re-)enabled, the
             * buffer's contents will be overwritten.
             * 
             * Note that DONE must be cleared in software; it is set by
             * hardware. Since we selected manual sampling and conversion, the
             * most-recent result is always in ADC1BUF0.
             */
            adc_value = ADC1BUF0;
            AD1CON1bits.DONE = 0;
            AD1CON1bits.SAMP = 1;
        }
        
        if (AD1CON1bits.SAMP) {
            /*
             * Wait 5 cycles before initiating conversion
             * 
             * If other tasks need to be done in the interim, a solution using
             * a counter to keep track of the number of iterations since last
             * completion is required.
             */
            asm volatile ("nop");
            asm volatile ("nop");
            asm volatile ("nop");
            asm volatile ("nop");
            asm volatile ("nop");
            AD1CON1bits.SAMP = 0;
        }
    }
    return 1;
}