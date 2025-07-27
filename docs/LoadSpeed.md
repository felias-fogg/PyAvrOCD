# Load Speed

| MCU              | dw-link | dw-link (H) | SNAP   | PICkit4 | Atmel-ICE | Power Debugger | JTAG-ICE3 | XPLAINED Mini 328P |
| ---------------- | ------- | ----------- | ------ | ------- | --------- | -------------- | --------- | ------------------ |
| mega328P (16MHz) | 0.6/4   | 1.0/5       | 0.7/12 | 0.6/6   | 1.0/14    | 1.0/14         | 0.7/13    | 0.3/3              |
| mega328P (8MHz)  | 0.6/4   | 1.0/5       | 0.7/12 | 0.6/6   | 1.0/14    | 1.0/14         | 0.7/13    |                    |
| mega328P(1MHz)   | 0.6/4   | 0.6/4       | 0.5/7  | 0.4/4   | 0.6/8     | 0.6/8          | 0.4/7     |                    |
| tiny85 (8MHz)    | 0.6/4   | 1.0/5       | 0.4/9  | 0.4/3   | 0.7/12    | 0.7/12         | 0.4/10    |                    |
| tiny85 (1MHz)    | 0.6/4   | 0.6/4       | 0.3/6  | 0.3/3   | 0.5/7     | 0.5/7          | 0.3/6     |                    |
| tiny1634 (8MHz)  | 0.6/4   | 1.0/6       | 0.3/4  | 0.2/2   | 0.6/8     | 0.6/8          | 0.3/7     |                    |
| tiny1634 (1MHz)  | 0.6/4   | 0.6/4       | 0.2/4  | 0.2/2   | 0.4/5     | 0.4/4          | 0.2/4     |                    |

Load speed is measured in kilobytes per second (kB/sec). The measurement was done on an M2 Mac.

The first number is the speed when using a load function that does not check whether the content is already loaded. The second number represents the speed for a load function that reads each page before writing, in the case where everything is already loaded. One could also consider this as "verification" speed. The actual speed will lie between these two numbers.

Dw-link (H) refers to dw-link using the high-speed option (250 kbps) for communication with the OCD.

To provide a perspective, the UNO bootloader programs an UNO at 7 kB/sec and verifies it at 10 kB/sec.
