// A sketch for testing timer modes
#include "ledsignal.h"

void setup(void)
{
  LedInit();
}

void loop(void)
{
  volatile unsigned long start, curr;

  LedOn();
  start=micros();
  curr=start;
  while (curr - start < 100000UL) {
    curr=micros();
  }
  LedOff();
  start=micros();
  curr=start;
  while (micros() - start < 100000UL) curr=micros();
}