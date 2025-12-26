// This is a sketch to test whether rangestepping works as advertised
// on JTAG targets (with four HWBPs). It will test whether
// 1) _delay_ms can be overstepped (without single instruction stepping)
// 2) a loop with four different exit points runs fast
// 3) a loop with five exit points is slow
// 4) a deadloop without any exit points runs fast (without single instruction stepping)

#include <util/delay.h>
#include "ledsignal.h"

volatile unsigned long cnt1, cnt2, cnt3;
volatile boolean stateoff;
unsigned long limit;


void LedToggle(void)
{
  if (stateoff) LedOff();
  else LedOn();
  stateoff = !stateoff;
}

void LedTrulyOff(void)
{
  stateoff = false;
  LedOff();
}

void setup(void)
{
  LedInit();
  LedOn();
  _delay_ms(300);
  LedOff();
  limit = 200/(16000000UL/F_CPU);
}

void loop(void)
{
  LedOn(); while (cnt1 < limit) { cnt1++; if ((cnt1 & 0x1FF) == 0x01FF) LedToggle(); if ((cnt1 & 0x1FE) == 0x1FE) LedOff(); if ((cnt1 & 0x1FC) == 0x1FC) LedOn(); };
  LedOff(); while (cnt2 < 100) { cnt2++; if ((cnt2 & 0xFF) == 9) LedToggle(); if ((cnt2 & 0xFF) == 9) LedOff(); if ((cnt2 & 0xFF) == 9) LedOn(); if ((cnt2 & 0xFF) == 9) LedTrulyOff();};
  LedOn(); while (1) { cnt3++; };
  return;
}