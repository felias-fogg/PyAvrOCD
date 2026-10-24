/*
 * For the e2e test 'reloadbp': a software breakpoint is hit and deleted, and a second program
 * is loaded before the target runs again. Probes that remove a cleared breakpoint only at the
 * next go or step (JTAGICE mkII, AVR Dragon) would then write the instruction of the first
 * program back into the second one. Both programs have the same layout; only the instruction at
 * reload_target differs: 'inc r24' (reload_var becomes 1) or, with -DSECOND, 'ldi r24, 0xA5'
 * (reload_var becomes 0xA5, opcode 0xEA85).
 */
#include <avr/io.h>
#include <stdint.h>

#ifdef SECOND
#define TARGET_INSTRUCTION "ldi r24, 0xA5\n"
#else
#define TARGET_INSTRUCTION "inc r24\n"
#endif

volatile uint8_t reload_var;

int main(void)
{
  while (1) {
    asm volatile(
      "clr r24\n"                /* so that reload_target is not main */
      ".global reload_target\n"
      "reload_target: " TARGET_INSTRUCTION
      ".global reload_next\n"
      "reload_next:   sts reload_var, r24\n"
      ".global reload_after\n"
      "reload_after:  nop\n"
      ::: "r24");
  }
}
