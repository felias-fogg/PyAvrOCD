#if defined(__AVR_ATmega48__) || defined(__AVR_ATmega48A__) || defined(__AVR_ATmega48P__) || \
  defined(__AVR_ATmega48PA__) ||   defined(__AVR_ATmega48PB__) || \
  defined(__AVR_ATmega88__) || defined(__AVR_ATmega88A__) || defined(__AVR_ATmega88P__) || \
  defined(__AVR_ATmega88PA__) ||   defined(__AVR_ATmega88PB__) || \
  defined(__AVR_ATmega168__) || defined(__AVR_ATmega168A__) || defined(__AVR_ATmega168P__) || \
  defined(__AVR_ATmega168PA__) ||   defined(__AVR_ATmega168PB__) || \
  defined(__AVR_ATmega328__) || defined(__AVR_ATmega328P__) || defined(__AVR_ATmega328PB__)
 #define LED1_PORT PORTB
 #define LED1_DDR  DDRB
 #define LED1      PB5
 #define LED2_PORT PORTB
 #define LED2_DDR  DDRB
 #define LED2      PB5
#elif defined(__AVR_AT90USB162__)
// LED on board
 #define LED1_PORT PORTD
 #define LED1_DDR  DDRD
 #define LED1      PD4
// SCK
 #define LED2_PORT PORTB
 #define LED2_DDR  DDRB
 #define LED2      PB1
#else
 #error "MCU is not supported"
#endif