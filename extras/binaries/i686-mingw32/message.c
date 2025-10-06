#include <stdio.h>
int main() {
  printf("Sorry, no built-in debugging support for 32-bit systems.\r\n"
	 "Download an avr-gdb version for your system from somewhere\r\n"
	 "and install PyAvrOCD with 'pipx install pyavrocd'.\r\n\r\n"
	 "If you see this error message on a 64-bit system, then\r\n"
	 "something went wrong when downloading the tool files.\r\n"
	 "Reinstall the board file and then try again.\r\n");
    }
