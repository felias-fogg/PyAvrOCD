# (Non-)Tri-state behavior of AVR programmers and debuggers

Measuring at Vcc=5V while the programmer/debugger is inactive or debugWIRE active (meaning the SPI part is inactive).

| Debugger        | MOSI idle | MISO idle | SCK idle   |
| --------------- | --------- | --------- | ---------- |
| Atmel-ICE       | H (w)     | H (vw)    | H (w)      |
| JTAGICE3        | Z         | Z         | L (w)      |
| PICkit4         | H (w)     | Z         | Z          |
| Power- debugger | H (w)     | H (vw)    | H (w)      |
| SNAP            | H (w)     | H (s)     | L (s)      |
| Arduino as ISP  | Z         | Z         | 0.5 V (vw) |
| Diamex          | Z         | H (w)     | H (w)      |
| USBasp          | Z         | Z         | Z          |

H = above 3 V

L = below 0.4 V

Z = below 0.4 V and driven up to almost Vcc by a 47 kΩ connected to Vcc

s = needs a 470 Ω pull-up/down resistor to override

w = needs a 4.7 kΩ pull-up/down resistor to override

vw = needs a 47 kΩ pull-up/down resistor to override

The behavior does not change when debugWIRE is active.