#include <avr/boot.h>
#include <avr/wdt.h>

#define SIGRD 5

void mcusr_init(void) __attribute__((naked)) __attribute__((section(".init3"))) __attribute__((used));
void mcusr_init(void)
{
  MCUSR = 0;
  wdt_disable();
}

int main(void)
{
  if (boot_signature_byte_get(0) != 0x1E) {
    boot_lock_bits_set (_BV (0));
  }
}