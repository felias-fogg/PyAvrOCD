
#ifndef VCC_H
#define VCC_H

#include <avr/eeprom.h>

#if  defined(__AVR_ATmega16M1__) || defined(__AVR_ATmega32M1__) || \
  defined(__AVR_ATmega64M1__) || defined(__AVR_ATmega32C1__) ||
  defined(__AVR_ATmega64C1__) || \
  defined(__AVR_AT90PWM1__) || defined(__AVR_AT90PWM2__) || defined(__AVR_AT90PWM2B__) || \
  defined(__AVR_AT90PWM3__) || defined(__AVR_AT90PWM3B__) || \
  defined(__AVR_AT90PVM81__) || defined(__AVR_AT90PVM161__) || \
  defined(__AVR_AT90PWM261__) || defined(__AVR_AT90PWM361__) 
#define DEFAULT_INTREF 2560
#elif defined(__AVR_ATmega8__)
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
