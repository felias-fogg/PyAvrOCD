// measure supply voltage
#include <stdlib.h>
#include "Vcc.h"

void success(void) {
  while (1);
}

void fail(void) {
  exit(3);
}

int main(void) {
  int result;
  Vcc vcc = Vcc();
  vcc.setIntref(DEFAULT_INTREF);
  result = vcc.measure(100);
  if (result < 2500 || result > 5500) { // This should not happen!
    fail();
  } else {
    success();
  }
  exit(0);
}

