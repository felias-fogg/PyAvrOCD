#include <Vcc.h>

int Vcc::_intref = 0;

int Vcc::measure(int repetition, int intref)
{
  int16_t reading;
  int32_t acc;
  uint8_t oldadcsra;
  uint8_t oldprr;


#if defined(__AVR_ATmega165__) || defined(__AVR_ATmega165A__) || defined(__AVR_ATmega165PA__) || \
  defined(__AVR_ATmega169__) || defined(__AVR_ATmega169A__) || defined(__AVR_ATmega169PA__) || \
  defined(__AVR_ATmega325__) || defined(__AVR_ATmega325A__) || defined(__AVR_ATmega325PA__) || \
  defined(__AVR_ATmega329__) || defined(__AVR_ATmega329A__) || defined(__AVR_ATmega329PA__) || \
  defined(__AVR_ATmega645__) || defined(__AVR_ATmega645A__) || defined(__AVR_ATmega645PA__) || \
  defined(__AVR_ATmega649__) || defined(__AVR_ATmega649A__) || defined(__AVR_ATmega649PA__) || \
  defined(__AVR_ATmega3250__) || defined(__AVR_ATmega3250A__) || defined(__AVR_ATmega3250PA__) || \
  defined(__AVR_ATmega3290__) || defined(__AVR_ATmega3290A__) || defined(__AVR_ATmega3290PA__) || \
  defined(__AVR_ATmega6450__) || defined(__AVR_ATmega6450A__) || defined(__AVR_ATmega6450PA__) || \
  defined(__AVR_ATmega6490__) || defined(__AVR_ATmega6490A__) || defined(__AVR_ATmega6490PA__) || \
  defined(__AVR_ATmega1280__) || defined(__AVR_ATmega2560__) || \
  defined(__AVR_ATmega1281__) || defined(__AVR_ATmega2561__) || \
  defined(__AVR_ATmega1284__) || defined(__AVR_ATmega1284P__) || \
  defined(__AVR_ATmega644__) || defined(__AVR_ATmega644A__) || \
  defined(__AVR_ATmega644P__) || defined(__AVR_ATmega644PA__) || \
  defined(__AVR_ATmega324__) || defined(__AVR_ATmega324A__) || \
  defined(__AVR_ATmega324PA__)	|| defined(__AVR_ATmega324P__) || \
  defined(__AVR_ATmega324PB__) || \
  defined(__AVR_ATmega164__) || defined(__AVR_ATmega164A__) || \
  defined(__AVR_ATmega164PA__) || defined(__AVR_ATmega164P__) || \
  defined(__AVR_ATmega16__) || defined(__AVR_ATmega32__) || defined(__AVR_ATmega16A__) || \
  defined(__AVR_ATmega32A__) || defined(__AVR_ATmega64__) || \
  defined(__AVR_ATmega64A__) ||  defined(__AVR_ATmega128__) ||	\
  defined(__AVR_ATmega128A__) || defined(__AVR_ATmega8535__) || \
  defined(__AVR_ATmega32U4__) || defined(__AVR_ATmega16U4__) || \
  defined(__AVR_AT90USB646__) ||   defined(__AVR_AT90USB647__) || \
  defined(__AVR_AT90USB1286__) ||   defined(__AVR_AT90USB1287__) || \

  ADMUX =  _BV(REFS0) | _BV(MUX4) | _BV(MUX3) | _BV(MUX2) | _BV(MUX1);
#elif defined(__AVR_ATmega328__) || defined(__AVR_ATmega328P__) || \
  defined(__AVR_ATmega328PB__) ||  defined (__AVR_ATmega168__) || \
  defined (__AVR_ATmega168A__)  || defined (__AVR_ATmega168PA__) || \
  defined (__AVR_ATmega168P__) || defined (__AVR_ATmega168PB__) || \
  defined (__AVR_ATmega88__) || defined (__AVR_ATmega88A__) || defined (__AVR_ATmega88P__)  || \
  defined (__AVR_ATmega88PA__) || defined (__AVR_ATmega88PB__) || \
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
#elif defined(__AVR_ATmega16M1__) || defined(__AVR_ATmega32M1__) || \
  defined(__AVR_ATmega64M1__) || defined(__AVR_ATmega32C1__) ||
  defined(__AVR_ATmega64C1__) 
    ADMUX = _BV(MUX4) | _BV(MUX0) | _BV(REFS0);
#elif defined(__AVR_AT90PWM1__) || defined(__AVR_AT90PWM2__) || defined(__AVR_AT90PWM2B__) || \
  defined(__AVR_AT90PWM3__) || defined(__AVR_AT90PWM3B__) || \
  defined(__AVR_AT90PVM81__) || defined(__AVR_AT90PVM161__) || \
    defined(__AVR_AT90PWM261__) || defined(__AVR_AT90PWM361__) 
    ADMUX = _BV(REFS0) | _BV(MUX3) | _BV(MUX2) | _BV(MUX1);
#elif  defined(__AVR_ATtiny2313__) || defined(__AVR_ATtiny2313A__) || \
  defined(__AVR_ATtiny4313__) ||				      \
  defined(__AVR_AT90USB82__) || defined(__AVR_AT90USB162__) || \
  defined(__AVR_ATmega32U2__) || defined(__AVR_ATmega16U2__) || \
  defined(__AVR_ATmega8U2__) 
  #error "This MCU does not have an ADC"
#elif  defined(__AVR_ATtiny13__) || defined(__AVR_ATmega8HVA__) || \
  defined(__AVR_ATmega16HVA__) ||  defined(__AVR_ATmega16HVB__) || \
  defined(__AVR_ATmega32HVB__) || defined(__AVR_ATmega16HVBrevB__) || \
  defined(__AVR_ATmega32HVBrevB__) || defined(__AVR_ATmega64HEV2__) ||  \
  defined(__AVR_ATmega64RFR2__) ||   defined(__AVR_ATmega128RFR2__) ||  \
  defined(__AVR_ATmega256RFR2__) || defined(__AVR_ATmega128RFA1) || \
  defined(__AVR_ATmega644RFR2__) ||   defined(__AVR_ATmega1284RFR2__) ||  \
  defined(__AVR_ATmega2564RFR2__) || defined(__AVR_ATmega406__)
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
