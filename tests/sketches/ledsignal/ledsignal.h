// This header file helps the test sketches to blink and to choose the right serial port
// It will blink on SCK and on LED_BUILTIN or another, MCU specific pins.
// If the sketch ends in an OK state, it will flash every 1.5 seconds for 0.2 seconds.
// If something went wrong, it will flash every 0.2 seconds for 0.2 seconds
// For the debugger, two routines are provided for testing the outcome.
#include <util/delay.h>
#ifdef SCK
  #define LED0 SCK
#endif
#if defined(__AVR_ATtiny13__) || defined(__AVR_ATtiny25__) || defined(__AVR_ATtiny45__) || \
  defined(__AVR_ATtiny85__)
#define LED1 4
#elif defined(__AVR_ATmega324PB__)
#define LED1 23
#define Serial Serial1
#elif defined(LED_BUILTIN)
  #define LED1 LED_BUILTIN
#else
  #warning "NO LED_BUILTIN or otherwise defined LED"
#endif


void OKBlink() {
  _delay_ms(1500);
}

void FailBlink() {
  _delay_ms(200);
}

void blink_exit (boolean OK) {
#ifdef LED0
  pinMode(LED0, OUTPUT);
#endif
#ifdef LED1
  pinMode(LED1, OUTPUT);
#endif
  while (1) {
#ifdef LED0
    digitalWrite(LED0, HIGH);
#endif
#ifdef LED1
    digitalWrite(LED1, HIGH);
#endif
    _delay_ms(200);
#ifdef LED0
    digitalWrite(LED0, LOW);
#endif
#ifdef LED1
    digitalWrite(LED1, LOW);
#endif
    if (OK) OKBlink();
    else FailBlink();
  }
}
