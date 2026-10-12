// -*- c++ -*-
// Sketch for tuning the INTREF value and programming it into EEPROM
// 1) Burn the fuses for EEPROM preservation 
// 2) Connect the Vcc and GND to a Voltage meter
// 3) Adjust the Intref value by typing in the commands and then save the value to EEPROM

#define BAUDRATE 9600
#define DEFAULT_INTREF 1100
#define VERSION "2.0"

#include <EEPROM.h>
#include <Vcc.h>
#include <stdio.h>
#include <stdlib.h>

#define LINEMAX 32

#ifdef INTREF_AT_END_OF_EEPROM
#define EE_ADDR (E2END-3)
#else
#define EE_ADDR 0
#endif


int intref;
int voltage;

void setup()
{
  EEPROM.get(EE_ADDR,intref);
  Serial.begin(BAUDRATE);
  while (!Serial);
  Serial.println(F("\r\ncalibrate V" VERSION "\n"));
  if ((unsigned int)intref == 0xFFFF) intref = DEFAULT_INTREF;
  voltage = Vcc::measure(1000, intref);
  printall();
}

void loop(void)
{
  char line[LINEMAX+1];
  char *succ;
  
  voltage = Vcc::measure(1000, intref);
  Serial.print(F("\nUse one of the following commands: \n\r\
 S      - show current INTREF value and Vcc\n\r\
 E      - save current INTREF value to EEPROM \n\r\
 I      - increase INTREF value by one \n\r\
 I<num> - increase INTREF by <num>\n\r\
 D      - decrease INTREF by one\n\r\
 D<num> - decrease INTREF by <num>\n\r\
Command: "));
  readline(line);
  Serial.println();
  switch (toupper(line[0])) {
  case 'S':
    voltage = Vcc::measure(1000, intref);
    printall();
    break;
  case 'E': Serial.print(F("Saving current INTREF value to EEPROM at address 0x"));
    Serial.println(EE_ADDR, HEX);
    EEPROM.put(EE_ADDR,intref);
    break;
  case 'I':
    if (line[1] == '\0') intref++;
    else intref += strtol(&line[1], &succ, 10);
    voltage = Vcc::measure(1000, intref);
    printall();
    break;
  case 'D': intref--;
    if (line[1] == '\0') intref--;
    else intref -= strtol(&line[1], &succ, 10);
    voltage = Vcc::measure(1000, intref);
    printall();
    break;
  default:
    Serial.print(F("Unknown command: "));
    Serial.println(line);
  }
}

void printall(void)
{
  Serial.print(F("INTREF="));
  Serial.print(intref);
  Serial.print(F(" Voltage="));
  Serial.print(voltage/1000);
  Serial.print(F("."));
  if ((voltage%1000) < 100) Serial.print(F("0"));
  if ((voltage%1000) < 10) Serial.print(F("0"));
  Serial.print(voltage%1000);
  Serial.println(F(" Volt"));
}

void readline(char buf[])
{
  byte ix = 0;
  char c = '\0';

  while (true) {
    if (Serial.available()) {
      c = Serial.read();
      if (c == '\n' || c == '\r') {
	buf[ix] = '\0';
	return;
      } else {
	buf[ix++] = c;
	Serial.print(c);
	if (ix >= LINEMAX) ix--;
      }
    }
  }
}
  
