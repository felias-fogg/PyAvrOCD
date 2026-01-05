// measure supply voltage
#include <Vcc.h>

void success(void) {
  while (1);
}

void fail(void) {
  exit(3);
}

void setup (void) {
  int result;
  Vcc vcc = Vcc();
  vcc.setIntref(DEFAULT_INTREF);
  result = vcc.measure(100);
  if (result < 2500 || result > 6800) { // sometimes accuracy seems to be low
    fail();
  } else {
    success();
  }
  exit(0);
}

void loop (void) { }
