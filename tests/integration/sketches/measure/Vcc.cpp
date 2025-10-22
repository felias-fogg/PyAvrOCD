#include <Vcc.h>

int Vcc::_intref = 0;

int Vcc::measure(int repetition, int intref)
{
  int16_t reading;
  int32_t acc;
  uint8_t oldadcsra;
  uint8_t oldprr;


#if defined(__AVR_ATmega1280__) || defined(__AVR_ATmega2560__)		\
  || defined(__AVR_ATmega1284__) || defined(__AVR_ATmega1284P__) || defined(__AVR_ATmega644__) || defined(__AVR_ATmega644A__)  \
  || defined(__AVR_ATmega644P__) || defined(__AVR_ATmega644PA__) || defined(__AVR_ATmega324__) || defined(__AVR_ATmega324A__) || defined(__AVR_ATmega324PA__)  \
  || defined(__AVR_ATmega324P__) || defined(__AVR_ATmega164__) || defined(__AVR_ATmega164A__) || defined(__AVR_ATmega164PA__) || defined(__AVR_ATmega164P__)  \
  || defined(__AVR_ATmega16__) || defined(__AVR_ATmega32__) || defined(__AVR_ATmega8535__) \
  || defined(__AVR_ATmega32U4__) || defined(__AVR_ATmega16U4__)
  ADMUX =  _BV(REFS0) | _BV(MUX4) | _BV(MUX3) | _BV(MUX2) | _BV(MUX1);
#elif defined(__AVR_ATmega328__) || defined(__AVR_ATmega328P__) ||  defined(__AVR_ATmega328PB__) || \
  defined (__AVR_ATmega168__) || defined (__AVR_ATmega168A__)  || defined (__AVR_ATmega168PA__) || \
  defined (__AVR_ATmega168P__) || defined (__AVR_ATmega168PB__) ||	\
  defined (__AVR_ATmega88__) || defined (__AVR_ATmega88A__) || defined (__AVR_ATmega88P__)  || \
  defined (__AVR_ATmega88PA__) || defined (__AVR_ATmega88PB__) ||	\
  defined (__AVR_ATmega48__) || defined (__AVR_ATmega48A__) || defined (__AVR_ATmega48P__) || \
  defined (__AVR_ATmega48PA__)|| defined (__AVR_ATmega48PB__) || defined(__AVR_ATmega8__)
  ADMUX = _BV(REFS0) | _BV(MUX3) | _BV(MUX2) | _BV(MUX1);
#elif  defined(__AVR_ATtiny43U__)   //ATtiny43U does not seem to work
  ADMUX = _BV(MUX2) || _BV(MUX0);
#elif  defined(__AVR_ATtiny24__) || defined(__AVR_ATtiny24A__) || defined(__AVR_ATtiny44__) \
  || defined(__AVR_ATtiny44A__) || defined(__AVR_ATtiny84__) || defined(__AVR_ATtiny84A__)
  ADMUX = _BV(MUX5) | _BV(MUX0);
#elif defined(__AVR_ATtiny441__) || defined(__AVR_ATtiny841__)
  ADMUXB = 0;
  ADMUXA = _BV(MUX3) | _BV(MUX2) | _BV(MUX0);
#elif defined(__AVR_ATtiny25__) || defined(__AVR_ATtiny45__) || defined(__AVR_ATtiny85__)
  ADMUX = _BV(MUX3) | _BV(MUX2);
#elif defined(__AVR_ATtiny261__) || defined(__AVR_ATtiny261A__) || defined(__AVR_ATtiny461__) \
  || defined(__AVR_ATtiny461A__) || defined(__AVR_ATtiny861__) || defined(__AVR_ATtiny861A__) \
  || defined(__AVR_ATtiny26__)
  ADMUX = _BV(MUX1) | _BV(MUX2) | _BV(MUX3) | _BV(MUX4);
#elif defined(__AVR_ATtiny167__) || defined(__AVR_ATtiny87__)
  ADMUX = _BV(MUX3) | _BV(MUX2);
#elif defined(__AVR_ATtiny48__) || defined(__AVR_ATtiny88__)
  ADMUX = _BV(REFS0) |  _BV(MUX3) | _BV(MUX2) | _BV(MUX1);
#elif defined(__AVR_ATtiny828__)
  ADMUXB = 0;
  ADMUXA = _BV(MUX0) | _BV(MUX2) | _BV(MUX3) | _BV(MUX4);
#elif defined(__AVR_ATtiny1634__)
  ADMUX = _BV(MUX3) | _BV(MUX2) | _BV(MUX0);
#elif  defined(__AVR_ATtiny2313__) || defined(__AVR_ATtiny2313A__) || defined(__AVR_ATtiny4313__) || \
  defined(__AVR_AT90USB82__) || defined(__AVR_AT90USB162__)
  #error "This MCU does not have an ADC"
#elif  defined(__AVR_ATtiny13__)
  #error "This MCU does not support measuring Vcc"
#else
  #error "Unsupported MCU"
#endif
#if defined(PRR)
  oldprr = PRR;
  PRR &= ~_BV(PRADC);
#elif defined(PRR0)
  oldprr = PRR0;
  PRR0 &= ~_BV(PRADC);
#endif
  oldadcsra = ADCSRA;
  ADCSRA |= _BV(ADEN);

  ADCSRA |= _BV(ADSC); // First conversion after enabling
  while (bit_is_set(ADCSRA,ADSC));

  acc = 0;
  for (int i = 0; i < repetition; i++) {
    ADCSRA |= _BV(ADSC); // Convert
    while (bit_is_set(ADCSRA,ADSC));
    reading = ADC;
    acc += ((intref * 1023L) / reading);
  }
  ADCSRA = oldadcsra;
#if defined(PRR)
  PRR = oldprr;
#elif defined(PRR0)
  PRR0 = oldprr;
#endif
  return acc/repetition;
}

int Vcc::measure(int repetition)
{
  return measure(repetition, (_intref ? _intref : (eeprom_read_word((unsigned int*)EE_INTREF) == 0xFFFF ?  DEFAULT_INTREF : eeprom_read_word((unsigned int*)EE_INTREF))));
}

void Vcc::setIntref(int intref)
{
  _intref = intref;
}
