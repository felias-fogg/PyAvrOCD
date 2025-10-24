// *****************
// debugWIRE targets
// *****************
#if defined(__AVR_AT90PWM1__) || defined(__AVR_AT90PWM2B__) || defined(__AVR_AT90PWM2B__) || \
  defined(__AVR_AT90PWM216__) || defined(__AVR_AT90PWM316) || \
  defined(__AVR_ATmega32C1__) ||   defined(__AVR_ATmega64C1__) || \
  defined(__AVR_ATmega16M1__) ||   defined(__AVR_ATmega32M1__) || defined(__AVR_ATmega64M1__)
 #define LED1_PORT PORTB
 #define LED1_DDR  DDRB
 #define LED1      PB7
#elif defined(__AVR_AT90PWM81__) || defined(__AVR_AT90PWM161__) || \
  defined(__AVR_ATmega16HVB__) || defined(__AVR_ATmega32HVB__) || \
  defined(__AVR_ATmega32HVE2__) || defined(__AVR_ATmega64HVE2__) 
 #define LED1_PORT PORTB
 #define LED1_DDR  DDRB
 #define LED1      PB5
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
 #define LED1_PORT PORTB
 #define LED1_DDR  DDRB
 #define LED1      PB1
#elif (__AVR_ATmega8U2__) ||  (__AVR_ATmega16U2__) ||  (__AVR_ATmega32U2__)
 #define LED1_PORT PORTB
 #define LED1_DDR  DDRB
 #define LED1      PB1
/* -- perhaps LED on NOOGROVE board ? */
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
/* -- perhaphs 0 on dev boards? */
#elif defined(__AVR_ATtiny13__) || defined(__AVR_ATtiny13A__) || \\
  defined(__AVR_ATtiny25__) || defined(__AVR_ATtiny45__) || defined(__AVR_ATtiny85__) 
// SCK
 #define LED1_PORT PORTB
 #define LED1_DDR  DDRB
 #define LED1      PB2
// LED on my dev boards
 #define LED2_PORT PORTB
 #define LED2_DDR  DDRB
 #define LED2      PB4
#elif defined(__AVR_ATtiny43U__)
// SCK
 #define LED1_PORT PORTB
 #define LED1_DDR  DDRB
 #define LED1      PB6
/* -- LED on dev board ? */
 #define LED2_PORT PORTA
 #define LED2_DDR  DDRA
 #define LED2      PA5
#elif defined(__AVR_ATtiny2313__) || defined(__AVR_ATtiny2313A__) || defined(__AVR_ATtiny4313__)
// SCK
 #define LED1_PORT PORTB
 #define LED1_DDR  DDRB
 #define LED1      PB7
// Builtin LED
 #define LED2_PORT PORTB
 #define LED2_DDR  DDRB
 #define LED2      PB4
#elif defined(__AVR_ATtiny24__) || defined(__AVR_ATtiny24A__) || \
   defined(__AVR_ATtiny44__) || defined(__AVR_ATtiny44A__) || \
   defined(__AVR_ATtiny84__) || defined(__AVR_ATtiny84A__) 
// SCK
 #define LED1_PORT PORTA
 #define LED1_DDR  DDRA
 #define LED1      PA4
/* - onboard LED ? */
#elif defined(__AVR_ATtiny441__) || defined(__AVR_ATtiny841__) 
 #define LED1_PORT PORTA
 #define LED1_DDR  DDRA
 #define LED1      PA4
/* - onboard LED ? */
#elif defined(__AVR_ATtiny261__) || defined(__AVR_ATtiny461__) || defined(__AVR_ATtiny861__) || \
 defined(__AVR_ATtiny261A__) || defined(__AVR_ATtiny461A__) || defined(__AVR_ATtiny861A__)
// SCK
 #define LED1_PORT PORTB
 #define LED1_DDR  DDRB
 #define LED1      PB2
/* -- LED on my dev boards ? */
 #define LED2_PORT PORTB
 #define LED2_DDR  DDRB
 #define LED2      PB6
#elif defined(__AVR__ATtiny87__) || defined(__AVR_ATtiny167__)
 #define LED1_PORT PORTA
 #define LED1_DDR  DDRA
 #define LED1      PA5
/* - onboard LED ? */
#elif defined(__AVR_ATtiny828__)
 #define LED1_PORT PORTD
 #define LED1_DDR  DDRD
 #define LED1      PD3
/* - onboard LED ? */
#elif defined(__AVR_ATtiny1634__)
 #define LED1_PORT PORTC
 #define LED1_DDR  DDRC
 #define LED1      PC1
/* - onboard LED ? */
// *****************
// Mega JTAG targets
// *****************
#elif defined(__AVR_ATmega16U4__) || defined(__AVR_ATmega32U4__)
// SCK
 #define LED1_PORT PORTB
 #define LED1_DDR  DDRB
 #define LED1      PB1
// Builtin LED 
 #define LED2_PORT PORTC
 #define LED2_DDR  DDRC
 #define LED2      PC7
#elif defined(__AVR_ATmega16__) || defined(__AVR_ATmega16A__) || \
  defined(__AVR_ATmega32__) || defined(__AVR_ATmega32A__) || \
  defined(__AVR_ATmega164A__) || defined(__AVR_ATmega164P__) || defined(__AVR_ATmega164PA__) || \
  defined(__AVR_ATmega324A__) || defined(__AVR_ATmega324P__) || defined(__AVR_ATmega324PA__) || \
  defined(__AVR_ATmega644A__) || defined(__AVR_ATmega644P__) || defined(__AVR_ATmega644PA__) || \
  defined(__AVR_ATmega1284__) || defined(__AVR_ATmega1284P__) 
// SCK
 #define LED1_PORT PORTB
 #define LED1_DDR  DDRB
 #define LED1      PB7
  /* -- Builtin LED on standard pinout ? */
 #define LED2_PORT PORTB
 #define LED2_DDR  DDRB
 #define LED2      PB0
#elif defined(__AVR_ATmega324PB__)
// SCK
 #define LED1_PORT PORTB
 #define LED1_DDR  DDRB
 #define LED1      PB7
// LED on XPLAINED board
 #define LED2_PORT PORTC
 #define LED2_DDR  DDRC
 #define LED2      PC7
#elif defined(__AVR_ATmega640__) || defined(__AVR_ATmega1280__) || defined(__AVR_ATmega2560__)
// SCK
 #define LED1_PORT PORTB
 #define LED1_DDR  DDRB
 #define LED1      PB1
// Builtin LED on Arduino Mega
 #define LED2_PORT PORTB
 #define LED2_DDR  DDRB
 #define LED2      PB7
#elif defined(__AVR_ATmega64__) || defined(__AVR_ATmega64A__) || \
  defined(__AVR_ATmega128__) || defined(__AVR_ATmega128A__) || \
  defined(__AVR_ATmega1281__) || defined(__AVR_ATmega2561__) || \
  defined(__AVR_AT90CAN32__) || defined(__AVR_AT90CAN64__) || defined(__AVR_AT90CAN128__) || \
  defined(__AVR_ATmega165A__) || defined(__AVR_ATmega165P__) || defined(__AVR_ATmega165PA__) || \
  defined(__AVR_ATmega169A__) || defined(__AVR_ATmega169P__) || defined(__AVR_ATmega169PA__) || \
  defined(__AVR_ATmega325A__) || defined(__AVR_ATmega325P__) || defined(__AVR_ATmega325PA__) || \
  defined(__AVR_ATmega329A__) || defined(__AVR_ATmega329P__) || defined(__AVR_ATmega329PA__) || \
  defined(__AVR_ATmega645A__) || defined(__AVR_ATmega645P__) || \
  defined(__AVR_ATmega649A__) || defined(__AVR_ATmega649P__) || \
  defined(__AVR_ATmega64RFR2__) || defined(__AVR_ATmega128RFR2__) || defined(__AVR_ATmega256RFR2__) || \
  defined(__AVR_ATmega644RFR2__) || defined(__AVR_ATmega1284RFR2__) || defined(__AVR_ATmega2564RFR2__) || \
  defined(__AVR_ATmega128RDFA1__)
// SCK
 #define LED1_PORT PORTB
 #define LED1_DDR  DDRB
 #define LED1      PB1
// Builtin LED in MegaCore
 #define LED2_PORT PORTB
 #define LED2_DDR  DDRB
 #define LED2      PB5
#elif defined(__AVR_ATmega3250__) || defined(__AVR_ATmega3250A__) || \
  defined(__AVR_ATmega3250P__) || defined(__AVR_ATmega3250PA__) || \
  defined(__AVR_ATmega3290__) || defined(__AVR_ATmega3290A__) || \
  defined(__AVR_ATmega3290P__) || defined(__AVR_ATmega3290PA__) || \
  defined(__AVR_ATmega6450__) || defined(__AVR_ATmega6450A__) || \
  defined(__AVR_ATmega6450P__) || \
  defined(__AVR_ATmega6490__) || defined(__AVR_ATmega6490A__) || \
  defined(__AVR_ATmega6490P__) 
// SCK
 #define LED1_PORT PORTB
 #define LED1_DDR  DDRB
 #define LED1      PB1
// Builtin LED in MegaCore
 #define LED2_PORT PORTB
 #define LED2_DDR  DDRB
 #define LED2      PB47
#elif defined(__AVR_ATmega162__)
// SCK
 #define LED1_PORT PORTB
 #define LED1_DDR  DDRB
 #define LED1      PB7
// Builtin LED in MajorCore
 #define LED2_PORT PORTB
 #define LED2_DDR  DDRB
 #define LED2      PB0
#elif defined(__AVR_ATmega406__)
 #warning "No info about SCK pin available; using PB1"
 #define LED1_PORT PORTB
 #define LED1_DDR  DDRB
 #define LED1      PB1
#elif defined(__AVR_AT90USB646__) || defined(__AVR_AT90USB647__) || \
  defined(__AVR_AT90USB1286__) || defined(__AVR_AT90USB1287__)
// SCK
 #define LED1_PORT PORTB
 #define LED1_DDR  DDRB
 #define LED1      PB1
#else
 #error "MCU is not supported"
#endif

#if defined(LED1) && !defined(LED2)
 #define LED2_PORT LED1_PORT
 #define LED2_DDR  LED1_DDR
 #define LED2      LED1
#endif
