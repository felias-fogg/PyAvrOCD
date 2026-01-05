#include <avr/io.h>
#include <avr/signature.h>

FUSES =
{
#ifdef LFUSE_DEFAULT
  .low = LFUSE_DEFAULT,
#endif
#ifdef HFUSE_DEFAULT
  .high = HFUSE_DEFAULT,
#endif
#ifdef EFUSE_DEFAULT
  .extended = EFUSE_DEFAULT,
#endif
};

LOCKBITS = (0);

int main()
{
  return 0;
}
