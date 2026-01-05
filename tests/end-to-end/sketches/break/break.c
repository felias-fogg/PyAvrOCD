// LED Blinker demo
// Blink on all known LED pins
// In the end stop on a break instruction and do not continue
#include <avr/io.h>
#include <util/delay.h>
#include "../includes/ledpindefs.h"

#define DELAYTIME 200

#define setBit(sfr, bit)     (_SFR_BYTE(sfr) |= (1 << bit))
#define clearBit(sfr, bit)   (_SFR_BYTE(sfr) &= ~(1 << bit))

void breakop() {
  asm("break");
}

int main(void) {

  // Init
  setBit(LED1_DDR, LED1);                      /* set LED pin for output */
  setBit(LED2_DDR, LED2);                      /* set LED pin for output */
  setBit(LED1_PORT, LED1);
  setBit(LED2_PORT, LED2);
  _delay_ms(DELAYTIME);
  clearBit(LED1_PORT, LED1);
  clearBit(LED2_PORT, LED2);
  _delay_ms(DELAYTIME);
  breakop();

  return 0;
}
