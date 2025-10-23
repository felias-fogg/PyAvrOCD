// debugWIRE targets
#if defined(__AVR_AT90PWM1__) || defined(__AVR_AT90PWM2B__) || defined(__AVR_AT90PWM2B__) || \
  defined(__AVR_AT90PWM216__) || defined(__AVR_AT90PWM316) || \
  defined(__AVR_ATmega32C1__) ||   defined(__AVR_ATmega64C1__) || \
  defined(__AVR_ATmega16M1__) ||   defined(__AVR_ATmega32M1__) || defined(__AVR_ATmega64M1__)
 PB7
#elif defined(__AVR_AT90PWM81__) || defined(__AVR_AT90PWM161__) || \
  defined(__AVR_ATmega16HVB__) || defined(__AVR_ATmega32HVB__) || \
  defined(__AVR_ATmega32HVE2__) || defined(__AVR_ATmega64HVE2__) 
 PB5
#elif defined(__AVR_AT90USB82__) || defined(__AVR_AT90USB162__)
// SCK
 #define LED1_PORT PORTB
 #define LED1_DDR  DDRB
 #define LED1      PB1
// LED on board
 #define LED2_PORT PORTD
 #define LED2_DDR  DDRD
 #define LED2      PD4
#elif defined(__AVR_ATmega8HVA__) || defined(__AVR_ATmega16HVA__)
 PB1
#elif (__AVR_ATmega8U2__) ||  (__AVR_ATmega16U2__) ||  (__AVR_ATmega32U2__)
 PB1
 perhaps LED on NOOGROVE board
#elif defined(__AVR_ATmega48__) || defined(__AVR_ATmega48A__) || defined(__AVR_ATmega48P__) || \
  defined(__AVR_ATmega48PA__) ||   defined(__AVR_ATmega48PB__) || \
  defined(__AVR_ATmega88__) || defined(__AVR_ATmega88A__) || defined(__AVR_ATmega88P__) || \
  defined(__AVR_ATmega88PA__) ||   defined(__AVR_ATmega88PB__) || \
  defined(__AVR_ATmega168__) || defined(__AVR_ATmega168A__) || defined(__AVR_ATmega168P__) || \
  defined(__AVR_ATmega168PA__) ||   defined(__AVR_ATmega168PB__) || \
  defined(__AVR_ATmega328__) || defined(__AVR_ATmega328P__) || defined(__AVR_ATmega328PB__) || \
  defined(__AVR_ATtiny48__) ||   defined(__AVR_ATtiny88__) 
 // SCK & LED on board
 #define LED1_PORT PORTB
 #define LED1_DDR  DDRB
 #define LED1      PB5
#elif defined(__AVR_ATtiny13__) || defined(__AVR_ATtiny13A__) || \\
  defined(__AVR_ATtiny25__) || defined(__AVR_ATtiny45__) || defined(__AVR_ATtiny85__) 
 PB2
 PB4 - on board
#elif defined(__AVR_ATtiny43U__)
 PB6
 -- onboard?
#elif defined(__AVR_ATtiny2313__) || defined(__AVR_ATtiny2313A__) || defined(__AVR_ATtiny4313__)
 PB7
#elif defined(__AVR_ATtiny24__) || defined(__AVR_ATtiny24A__) || \
   defined(__AVR_ATtiny44__) || defined(__AVR_ATtiny44A__) || \
   defined(__AVR_ATtiny84__) || defined(__AVR_ATtiny84A__) 
 PA4
 - onboard?
#elif defined(__AVR_ATtiny441__) || defined(__AVR_ATtiny841__) 
 PA4
 - onboard?
#elif defined(__AVR_ATtiny261__) || defined(__AVR_ATtiny461__) || defined(__AVR_ATtiny861__) || \
 defined(__AVR_ATtiny261A__) || defined(__AVR_ATtiny461A__) || defined(__AVR_ATtiny861A__)
 PB2
 - onboard?
#elif defined(__AVR__ATtiny87__) || defined(__AVR_ATtiny167__)
 PA5
 - onboard?
#elif defined(__AVR_ATtiny828__)
 PD3
 - onboard?
#elif defined(__AVR_ATtiny1634__)
 PC1
 - onboard?
 // Mega JTAG targets
#elif defined(__AVR_ATmega16U4__) || defined(__AVR_ATmega32U4__)
 PB1
 - onboard?
#elif defined(__AVR_ATmega16__) || defined(__AVR_ATmega16A__) || \
  defined(__AVR_ATmega32__) || defined(__AVR_ATmega32A__) || \
  defined(__AVR_ATmega164A__) || defined(__AVR_ATmega164P__) || defined(__AVR_ATmega164PA__) || \
  defined(__AVR_ATmega324A__) || defined(__AVR_ATmega324P__) || defined(__AVR_ATmega324PA__) || \
  defined(__AVR_ATmega644A__) || defined(__AVR_ATmega644P__) || defined(__AVR_ATmega644PA__) || \
  defined(__AVR_ATmega1284__) || defined(__AVR_ATmega1284P__) 
  PB7
  - onboard?
#else
 #error "MCU is not supported"
#endif

#if defined(LED1) && !defined(LED2)
 #define LED2_PORT LED1_PORT
 #define LED2_DDR  LED1_DDR
 #define LED2      LED1
#endif
