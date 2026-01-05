// LED Blinker demo
// Blink on all known LEAD pins
#include <avr/io.h>
#include <util/delay.h>
#include "../includes/ledpindefs.h"

#define DELAYTIME 100

#define setBit(sfr, bit)     (_SFR_BYTE(sfr) |= (1 << bit))
#define clearBit(sfr, bit)   (_SFR_BYTE(sfr) &= ~(1 << bit))


int main(void) {

  // Init
  setBit(LED1_DDR, LED1);                      /* set LED pin for output */
  setBit(LED2_DDR, LED2);                      /* set LED pin for output */

  // Mainloop
  while (1) {

    setBit(LED1_PORT, LED1);
    setBit(LED2_PORT, LED2);
    _delay_ms(DELAYTIME);

    clearBit(LED1_PORT, LED1);
    clearBit(LED2_PORT, LED2);
    _delay_ms(DELAYTIME);

  }
  return 0;                                          /* end mainloop */
}
