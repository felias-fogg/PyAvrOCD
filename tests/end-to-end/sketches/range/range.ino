// This is a sketch to test whether rangestepping works as advertised
// on debugWIRE targets (with one HWBP only). It will test whether
// 1) _delay_ms can be overstepped (without single instruction stepping)
// 2) a loop with a function call can be executed fast by over-stepping the call (after
//    having it executed once) -- does not apply to dw-link!
// 3) a loop with two different exit points (regular + return) uses single instruction stepping
// 4) a deadloop without any exit points runs fast (without single instruction stepping)
// For UPDI and JTAG targets, HWBP-only mode is used and 1 or 3 HWBPS are allocated

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
  while (cnt < 3000) {cnt++; if ((cnt & 7) == 1) LedToggle();  };
  LedOff();
  cnt = 0;
  while (cnt < 3000) {cnt++; if ((cnt & 0xFF) == 0) return;  };
  cnt = 0;
  while (1) { cnt++; };
  return;
}