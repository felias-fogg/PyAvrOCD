// Does the AVR8X ADC ignore the documented 16-bit write order for CPU accesses
// as well, or only for accesses through UPDI while the target is halted?
//
// For each of ADC0.WINHT (the suspect) and TCB0.CCMP (the control) the three
// write variants are executed by the CPU and the result is read back:
//
//   single      one 16-bit store, the order is the compiler's choice
//               (check adcwin.lst: avr-gcc writes the low byte first)
//   low_first   two byte stores, low byte first - the documented order
//   high_first  two byte stores, high byte first
//
// Expected for a register that behaves as documented (8.5.6 of the data sheet):
//   single = 0x1234, low_first = 0x1234, high_first = 0x1200
// Expected if the ADC anomaly also applies to CPU accesses:
//   single = 0x1200, low_first = 0x1200, high_first = 0x1234

#include <avr/io.h>
#include <stdint.h>

typedef struct {
  uint16_t single;
  uint16_t low_first;
  uint16_t high_first;
} result_t;

volatile result_t winht_result;
volatile result_t ccmp_result;

// Read back the way the data sheet prescribes: low byte first
static uint16_t read_back(volatile uint8_t *lo, volatile uint8_t *hi)
{
  uint8_t l = *lo;
  uint8_t h = *hi;
  return ((uint16_t)h << 8) | l;
}

// Clear the register with the low, high, low sequence, which empties it
// under both behaviors
static void clear_reg(volatile uint8_t *lo, volatile uint8_t *hi)
{
  *lo = 0;
  *hi = 0;
  *lo = 0;
}

static void measure(volatile uint16_t *reg, volatile result_t *res)
{
  volatile uint8_t *lo = (volatile uint8_t *)reg;
  volatile uint8_t *hi = lo + 1;

  clear_reg(lo, hi);
  *reg = 0x1234;
  res->single = read_back(lo, hi);

  clear_reg(lo, hi);
  *lo = 0x34;
  *hi = 0x12;
  res->low_first = read_back(lo, hi);

  clear_reg(lo, hi);
  *hi = 0x12;
  *lo = 0x34;
  res->high_first = read_back(lo, hi);
}

// Breakpoint location: the results are complete when this is reached
__attribute__((noinline)) void done(void)
{
  asm volatile ("nop");
}

int main(void)
{
  measure(&ADC0.WINHT, &winht_result);
  measure(&TCB0.CCMP, &ccmp_result);

  while (1) {
    done();
  }
  return 0;
}
