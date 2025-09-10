#include <Arduino.h>
#if defined(__AVR_ATtiny13__)
#define IRQPIN 1
#elif defined(__AVR_ATtiny2313__) ||  defined(__AVR_ATtiny4313__) || defined(__AVR_ATtiny2313A__)
#define IRQPIN 4
#elif defined(__AVR_ATtiny43U__)
#define IRQPIN 7
#elif defined(__AVR_ATtiny24__) || defined(__AVR_ATtiny44__) || defined(__AVR_ATtiny84__)
#define IRQPIN 8
#elif defined(__AVR_ATtiny441__) || defined(__AVR_ATtiny841__)
#define IRQPIN 1
#elif defined(__AVR_ATtiny25__) || defined(__AVR_ATtiny45__) || defined(__AVR_ATtiny85__)
#define IRQPIN 2
#elif defined(__AVR_ATtiny261__) || defined(__AVR_ATtiny461__) || defined(__AVR_ATtiny861__)
#define IRQPIN 14
#elif defined(__AVR_ATtiny87__) || defined(__AVR_ATtiny167__)
#define IRQPIN 14
#elif defined(__AVR_ATtiny48__) || defined(__AVR_ATtiny88__)
#define IRQPIN 2
#elif defined(__AVR_ATtiny828__)
#define IRQPIN 17
#elif defined(__AVR_ATtiny1634__)
#define IRQPIN 11
#elif defined(__AVR_ATmega48__) || defined(__AVR_ATmega48A__) || \
  defined(__AVR_ATmega48P__) || defined(__AVR_ATmega48PA__) || defined(__AVR_ATmega48PB__) || \
  defined(__AVR_ATmega88__) || defined(__AVR_ATmega88A__) ||  \
  defined(__AVR_ATmega88P__) || defined(__AVR_ATmega88PA__) || defined(__AVR_ATmega88PB__) || \
  defined(__AVR_ATmega168__) || defined(__AVR_ATmega168A__) ||  \
  defined(__AVR_ATmega168P__) || defined(__AVR_ATmega168PA__) || defined(__AVR_ATmega168PB__) || \
  defined(__AVR_ATmega328__) || defined(__AVR_ATmega328P__) || defined(__AVR_ATmega328PB__)
#define IRQPIN 2
#elif defined(__AVR_ATmega640__) || defined(__AVR_ATmega1280__) || defined(__AVR_ATmega2560__)
// Mega pinout (default)
#define IRQPIN 21
#elif defined(__AVR_ATmega64__) || defined(__AVR_ATmega128__) || \
  defined(__AVR_ATmega128__) || defined(__AVR_ATmega2560__) ||	 \
  defined(__AVR_AT90CAN32__) || defined(__AVR_AT90CAN64__) || defined(__AVR_AT90CAN128__)
#define IRQPIN 18
#elif defined(__AVR_ATmega169__) || defined(__AVR_ATmega169A__) || \
  defined(__AVR_ATmega169P__) || defined(__AVR_ATmega169PA__) || \
  defined(__AVR_ATmega329__) || defined(__AVR_ATmega329A__) || \
  defined(__AVR_ATmega329P__) || defined(__AVR_ATmega329PA__) || \
  defined(__AVR_ATmega649__) || defined(__AVR_ATmega649A__) || \
  defined(__AVR_ATmega649P__) || defined(__AVR_ATmega649PA__) || \
  defined(__AVR_ATmega165__) || defined(__AVR_ATmega165A__) || \
  defined(__AVR_ATmega165P__) || defined(__AVR_ATmega165PA__) || \
  defined(__AVR_ATmega325__) || defined(__AVR_ATmega325A__) || \
  defined(__AVR_ATmega325P__) || defined(__AVR_ATmega325PA__) || \
  defined(__AVR_ATmega645__) || defined(__AVR_ATmega645A__) || \
  defined(__AVR_ATmega645P__) || defined(__AVR_ATmega645PA__)
#define IRQPIN 19
#elif defined(__AVR_ATmega3290__) || defined(__AVR_ATmega3290A__) || \
  defined(__AVR_ATmega3290P__) || defined(__AVR_ATmega3290PA__) || \
  defined(__AVR_ATmega6490__) || defined(__AVR_ATmega6490A__) || \
  defined(__AVR_ATmega6490P__) || defined(__AVR_ATmega6490PA__) || \
  defined(__AVR_ATmega3250__) || defined(__AVR_ATmega3250A__) || \
  defined(__AVR_ATmega3250P__) || defined(__AVR_ATmega3250PA__) || \
  defined(__AVR_ATmega6450__) || defined(__AVR_ATmega6450A__) || \
  defined(__AVR_ATmega6450P__) || defined(__AVR_ATmega6450PA__)
#define IRQPIN 26
#elif defined(__AVR_ATmega16__) || defined(__AVR_ATmega16A__) ||  \
  defined(__AVR_ATmega32__) || defined(__AVR_ATmega32A__) ||  \
  defined(__AVR_ATmega164__) || defined(__AVR_ATmega164A__) ||	 \
  defined(__AVR_ATmega164P__) || defined(__AVR_ATmega164PA__) || \
  defined(__AVR_ATmega324__) || defined(__AVR_ATmega324A__) ||	 \
  defined(__AVR_ATmega324P__) || defined(__AVR_ATmega324PA__) || defined(__AVR_ATmega324PB__) || \
  defined(__AVR_ATmega644__) || defined(__AVR_ATmega644A__) ||	 \
  defined(__AVR_ATmega644P__) || defined(__AVR_ATmega644PA__) || \
  defined(__AVR_ATmega1284__) || defined(__AVR_ATmega1284A__) || \
  defined(__AVR_ATmega1284P__) || defined(__AVR_ATmega1284PA__)
#define IRQPIN 10
#elif defined(__AVR_ATmega162__) || defined(__AVR_ATmega162A__) || \
  defined(__AVR_ATmega162P__) || defined(__AVR_ATmega162PA__)
#define IRQPIN 10
#else
#error "MCU not supported"
#endif

volatile int irqcount = 0;
volatile int outsidecount = 0;

void setup()
{
#if FLASHEND >= 4095
  Serial.begin(38400);
  Serial.println(F("Startup ..."));
  delay(500);
#endif
  pinMode(IRQPIN, OUTPUT);
  digitalWrite(IRQPIN, LOW);
  attachInterrupt(0, irqserver, LOW);
}

void loop()
{
  digitalWrite(IRQPIN, LOW);
  shortwait(1);
  outsidecount++;
  digitalWrite(IRQPIN, HIGH);
  delay(200); // necessary to give enough time for printing!
#if FLASHEND >= 4095
  Serial.print("IRQ count: ");
  Serial.println(irqcount);
#endif
}

void shortwait(unsigned long ms)
{
  delay(ms);
}

void irqserver()
{
  irqcount++;
}
