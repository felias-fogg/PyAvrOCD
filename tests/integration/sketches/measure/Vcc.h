
#ifndef VCC_H
#define VCC_H

#include <avr/eeprom.h>

#if defined(__AVR_ATmega8__)
#define DEFAULT_INTREF 1300
#elif defined(__AVR_ATtiny26__)
#define DEFAULT_INTREF 1180
#elif defined(__AVR_ATmega16__) || defined(__AVR_ATmega32__) || defined(__AVR_ATmega8535__)
#define DEFAULT_INTREF 1230
#else
#define DEFAULT_INTREF 1100
#endif

#define EE_INTREF (E2END-3)

class Vcc {
 public:
  static int measure(int repetition=10);
  static int measure(int repetition, int intref);
  static void setIntref(int intref);
 private:
  static int _intref;
};
#endif
