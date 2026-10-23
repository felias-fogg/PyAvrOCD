/*
 * For the e2e test 'setpc' (UPDI only): the PC is written onto a software breakpoint
 * and the target is single-stepped. The labels give GDB fixed names for the three
 * instructions, wherever the compiler puts them: a one-word instruction that gets
 * the breakpoint, a two-word one after it, and one more after that. When the step
 * goes wrong, it lands at pcbp_next+2, the middle of the two-word instruction.
 */
#include <avr/io.h>
#include <stdint.h>

volatile uint8_t pcbp_var;

int main(void)
{
  while (1) {
    asm volatile(
      "nop\n"                    /* so that pcbp_target is not main */
      ".global pcbp_target\n"
      "pcbp_target:  inc r24\n"
      ".global pcbp_next\n"
      "pcbp_next:    sts pcbp_var, r24\n"
      ".global pcbp_after\n"
      "pcbp_after:   nop\n"
      ::: "r24");
  }
}
