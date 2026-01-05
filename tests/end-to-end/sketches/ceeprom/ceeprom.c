#include <stdlib.h>
#include <stdbool.h>
#include <avr/eeprom.h>

bool OK = true;

uint8_t ee_data[] EEMEM = "Data that's loaded straight into EEPROM\n";

uint8_t ver[41] = "Data that's loaded straight into EEPROM\n";


void success(void) {
  while (1);
}

void fail(void) {
  exit(3);
}

void final(bool OK) {
  if (OK) success();
  else fail();
}

void setup() {
  eeprom_write_byte(ee_data, 'd');
  ver[0] = 'd';
}

void loop() {
  char c;
  int i = 0;
  uint8_t *ptr = ee_data;

  while (eeprom_read_byte(ptr)) {
    c = eeprom_read_byte(ptr++);
    if (ver[i++] != c)
      OK = false;
  }
  final(OK);
}

int main(void) {
  setup();
  loop();
}
