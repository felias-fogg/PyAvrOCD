# Load Speed

| MCU              | dw-link | dw-link (H) | SNAP   | PICkit4 | Atmel-ICE | Power Debug-ger | JTAG-ICE3 | XPLAINED Mini 328P | Uno Boot-loader |
| ---------------- | ------- | ----------- | ------ | ------- | --------- | --------------- | --------- | ------------------ | --------------- |
| mega328P (16MHz) | 0.6/4   | 1.0/5       | 0.7/12 | 0.6/6   | 1.0/14    | 1.0/14          | 0.7/13    | 0.3/3              | 7/10            |
| mega328P (8MHz)  | 0.6/4   | 1.0/5       | 0.7/12 | 0.6/6   | 1.0/14    | 1.0/14          | 0.7/13    |                    |                 |
| mega328P(1MHz)   | 0.6/4   | 0.6/4       | 0.5/7  | 0.4/4   | 0.6/8     | 0.6/8           | 0.4/7     |                    |                 |
| tiny85 (8MHz)    | 0.6/4   | 1.0/5       | 0.4/9  | 0.4/3   | 0.7/12    | 0.7/12          | 0.4/10    |                    |                 |
| tiny85 (1MHz)    | 0.6/4   | 0.6/4       | 0.3/6  | 0.3/3   | 0.5/7     | 0.5/7           | 0.3/6     |                    |                 |
| tiny1634 (8MHz)  | 0.6/4   | 1.0/6       | 0.3/4  | 0.2/2   | 0.6/8     | 0.6/8           | 0.3/7     |                    |                 |
| tiny1634 (1MHz)  | 0.6/4   | 0.6/4       | 0.2/4  | 0.2/2   | 0.4/5     | 0.4/4           | 0.2/4     |                    |                 |

Load speed is measured in kB/sec. The measurement was done on an M2 Mac.

The first number is the speed when using a load function that does not check whether the content is already loaded. The second number is the speed for a load function that reads before it writes in case everything is already loaded. One could also consider this as "verification" speed. The actual speed will lie between these two numbers.

Dw-link (H) means dw-link using the high-speed option (250kbps) for communication with the OCD. The Microchip debuggers apparently also use such an option.

In order to provide a perspective, the UNO bootloader programs an UNO with 7kB/sec and verifies it with 10kB/sec.
