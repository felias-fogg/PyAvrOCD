// Demonstrate Vcc::measure

#include <Vcc.h>
#include <EEPROM.h>

#define BAUDRATE 9600

int intref;

void setup(void)
{
  Serial.begin(BAUDRATE);
  while (!Serial);
  EEPROM.get(EE_INTREF, intref);
}

void loop(void)
{
  int voltage;
  voltage = Vcc::measure(1000,1100);
  Serial.print(F("Vcc (uncalibrated): "));
  Serial.print(voltage);
  Serial.println(F(" mV"));
  if ((unsigned int)intref != 0xFFFF) {
    voltage = Vcc::measure(1000);
    Serial.print(F("Vcc (calibrated):   "));
    Serial.print(voltage);
    Serial.println(F(" mV"));
    Serial.print(F("Internal Reference: "));
    Serial.print(intref);
    Serial.println(F(" mV"));
  }
  Vcc::setIntref(1050); // set intref value globally ('overrides' value in EEPROM!)
  Serial.print(F("Vcc (calibrated with a global value of 1050): "));
  Serial.print(Vcc::measure(1000));
  Serial.println(F(" mV"));
  while (1);
}
