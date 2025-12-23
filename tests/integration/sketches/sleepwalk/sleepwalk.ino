// sketch to test sleep walking
#include <util/delay.h>
#include <avr/sleep.h>
#include <Arduino.h>
#include "ledsignal.h"


void deepSleep(byte mode)
{
  set_sleep_mode(mode);
  cli();
  sleep_enable();
  sei();
  sleep_cpu();
  sleep_disable();
  sei();
}


void setup(void)
{
  LedInit();
  LedOff();
}

void loop (void)
{
  _delay_ms(300);
  LedOn();
  deepSleep(SLEEP_MODE_PWR_DOWN);
  LedOff();
}