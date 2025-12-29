// This is a sketch to test whether rangestepping works as advertised
// on denbugWIRE targets (with one HWBP only). It will test whether
// 1) _delay_ms can be overstepped (without single instruction stepping)
// 2) a deadloop without any exit points runs fast (without single instruction stepping)
// 3) a loop with two different exit points uses single instruction stepping

#include <util/delay.h>
#include "ledsignal.h"

volatile unsigned long cnt;

void LedToggle(void)
{
  static boolean stateoff;
  if (stateoff) LedOff();
  else LedOn();
  stateoff = !stateoff;
}

void setup(void)
{
  LedInit();
  LedOn();
  _delay_ms(300);
  LedOff();
}

void loop(void)
{
  cnt = 0;
  while (cnt < 30) { cnt++; if ((cnt & 7) == 0) LedToggle(); };
  LedOff();
  cnt = 0;
  while (1) { cnt++; };
  return;
}