#include <avr/boot.h>
#include <util/delay.h>
#include <avr/wdt.h>

#define cell8 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF
#define cell64 cell8, cell8, cell8, cell8, cell8, cell8, cell8, cell8
#define cell256 cell64, cell64, cell64, cell64
#define cell1024 cell256, cell256, cell256, cell256
#define cell2048 cell1024, cell1024
#define cell7168 cell2048, cell2048, cell2048, cell1024

#define SIGRD 5

const uint8_t cell[] PROGMEM = { cell7168 };
uint16_t celladdr;
void mcusr_init(void) __attribute__((naked)) __attribute__((section(".init3"))) __attribute__((used));
void mcusr_init(void)
{
  MCUSR = 0;
  wdt_disable();
}

int main(void)
{
  if (boot_signature_byte_get(0) != 0x1E) {
    boot_lock_bits_set (_BV (BLB01));
  }

  PORTB = pgm_read_byte(&cell);
}