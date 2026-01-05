#include <Arduino.h>
#include "irqpin.h"

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
