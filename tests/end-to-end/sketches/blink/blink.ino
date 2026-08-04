// Program intended to be used for testing pyavrocd
#include "ledsignal.h"

volatile byte cycle = 0; // cycle counter
volatile unsigned long privmillis = 0;

#ifdef TCB0_INT_vect // Modern MCU
// Set up TCB0 for periodic interrupt
// Define the ISR
ISR(TCB0_INT_vect) {
  // Your code here
  TCB0.INTFLAGS = TCB_CAPT_bm;    // Clear the interrupt flag
  irq_routine();
}
#else // Classic MCU
#ifdef TIM0_COMPA_vect
ISR(TIM0_COMPA_vect)
#elif defined(TIMER0_COMPA_vect)
ISR(TIMER0_COMPA_vect)
#else
ISR(TIMER0_COMP_vect)
#endif
{
  irq_routine();
}
#endif

void irq_routine(void) {
  if (cycle < 5)
    privmillis += (20000000UL/F_CPU);
  else
    privmillis += (20000000UL/F_CPU)*5; // time is 5 times faster!
}

unsigned long mymillis(void) {
  byte savesreg = SREG;
  unsigned long now;
  cli();
  now = privmillis;
  SREG = savesreg;
  return now;
}

void mydelay(unsigned long wait) {
  unsigned long start = mymillis();

  while (mymillis() - start < wait);
}

void test_cycle() {
  if (++cycle >= 10) cycle = 0;  // cyclic counter
}

void setup() {
  LedInit();   // initialize digital pin LED as an output.

#ifdef TCB0 // Modern MCU
  TCB0.CTRLB = TCB_CNTMODE_INT_gc;  // Periodic interrupt mode
  TCB0.CCMP = F_CPU/1000;           // Set interval for one milli second
  TCB0.INTCTRL = TCB_CAPT_bm;       // Enable interrupt
  TCB0.CTRLA = TCB_ENABLE_bm;       // Enable timer
#else      // Classic MCU
#ifdef OCR0A
  OCR0A = 0x80;           // prepare for having a COMPA interrupt
#else
  OCR0 = 0x80;           // prepare for having a COMP interrupt
#endif
#ifdef TIMSK
  #ifdef OCIE0A
      TIMSK |= _BV(OCIE0A);   // enable COMPA interrupt on Timer0
  #else
      TIMSK |= _BV(OCIE0);   // enable COMP interrupt on Timer0
  #endif
#else
  TIMSK0 |= _BV(OCIE0A);  // enable COMPA interrupt on Timer0
#endif
#ifdef __AVR_ATtiny13__   // set prescaler on ATtiny13, since the ATtiny13 does not initialize TCCR0B by itself
#if F_CPU >= 8000000
  TCCR0B = 0x03;         // prescaler 64 on fast Attinys
#else
  TCCR0B = 0x02;         // set prescaler 8 on slow ATtinys
#endif
#endif
#endif
  // now force that the interrupt is actually used
  volatile unsigned long start = millis();
  start += 100;
  start = start/millis();
}

// the loop function runs over and over again forever
void loop() {
  LedOn();                       // turn the LEDs on (HIGH is the voltage level)
  mydelay(100);                 // wait for approximately one second or 1/5 of a second
  LedOff();                      // turn the LEDs off by making the voltage LOW
  delay(100);                   // wait for a second
  test_cycle();                  // test and reset cyclic counter
}
