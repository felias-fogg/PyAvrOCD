# Load Speed

The time to upload a new version of the firmware is, of course, a critical factor in the development process. Interestingly, there is a wide variation. In the tables below, you find numbers for a number of different configurations. All measurements are in kB/sec as reported by GDB's load function.

The first number in each pair gives the speed when verification of uploaded code is switched off (`monitor verify disable`), the second number is for the case that this option is switched on (`monitor verify enable`). The first line in each cell is the speed of loading without a prior check of whether the code is already loaded (`monitor load writeonly`), while the second and third lines give the speed for read-before-write (`monitor load readbeforewrite`). The second line shows the worst case, i.e., no loaded page is identical with the file to be loaded, and the third line shows the best case, i.e., no page had to be loaded.

The first table is about debugWIRE targets. Dw-link (H) refers to dw-link using the high-speed option (250 kbps) for communication with the OCD. To provide a perspective, the UNO bootloader programs an UNO at 7 kB/sec and verifies it at 10 kB/sec. As one can see, having verification switched on does not slow down anything. Further, even in the worst case, read-before-write is not slower than blind writing. 

| MCU              | dw-link              | dw-link (H)          | SNAP                   | PICkit4             | Atmel-ICE              | Power Debug-ger        | JTAG-ICE3             | XPLAI-NED Mini 328P |
| ---------------- | -------------------- | -------------------- | ---------------------- | ------------------- | ---------------------- | ---------------------- | --------------------- | ------------------- |
| mega328P (16MHz) | 0.6/0.6  0.6/0.6 4/4 | 1.0/1.0 1.0/1.0 5/5  | 0.7/0.7  0.7/0.7 12/12 | 0.6/0.6 0.6/0.6 6/6 | 1.0/1.0 1.0/1.0 14/14  | 1.0/1.0 1.0/1.0 14/14  | 0.7/0.7 0.7/0.7 13/13 | 0.3/0.3 0.3/0.3 3/3 |
| mega328P (8MHz)  | 0.6/0.6  0.6/0.6 4/4 | 1.0/1.0 1.0/1.0 5/5  | 0.7/0.7  0.7/0.7 12/12 | 0.6/0.6 0.6/0.6 6/6 | 1.0/1.0 1.0/1.0 14/14  | 1.0/1.0 1.0/1.0 14/14  | 0.7/0.7 0.7/0.7 13/13 |                     |
| mega328P(1MHz)   | 0.6/0.6  0.6/0.6 4/4 | 0.6/0.6  0.6/0.6 4/4 | 0.5/0.5 0.5/0.5 7/7    | 0.4/0.4 0.4/0.4 4/4 | 0.6/0.6  0.6/0.6 8/8   | 0.6/0.6  0.6/0.6 8/8   | 0.4/0.4 0.4/0.4 7/7   |                     |
| tiny85 (8MHz)    | 0.6/0.6  0.6/0.6 4/4 | 1.0/1.0 1.0/1.0 5/5  | 0.4/0.4 0.4/0.4 9/9    | 0.4/0.4 0.4/0.4 3/3 | 0.7/0.7  0.7/0.7 12/12 | 0.7/0.7  0.7/0.7 12/12 | 0.4/0.4 0.4/0.4 10/10 |                     |
| tiny85 (1MHz)    | 0.6/0.6  0.6/0.6 4/4 | 0.6/0.6  0.6/0.6 4/4 | 0.3/0.3 0.3/0.3 6/6    | 0.3/0.3 0.3/0.3 3/3 | 0.5/0.5 0.5/0.5 7/7    | 0.5/0.5 0.5/0.5 7/7    | 0.3/0.3 0.3/0.3 6/6   |                     |
| tiny1634 (8MHz)  | 0.6/0.6  0.6/0.6 4/4 | 1.0/1.0 1.0/1.0 6/6  | 0.3/0.3 0.3/0.3 4/4    | 0.2/0.2 0.2/0.2 2/2 | 0.6/0.6  0.6/0.6 8/8   | 0.6/0.6  0.6/0.6 8/8   | 0.3/0.3 0.3/0.3 7/7   |                     |
| tiny1634 (1MHz)  | 0.6/0.6  0.6/0.6 4/4 | 0.6/0.6  0.6/0.6 4/4 | 0.2/0.2 0.2/0.2 4/4    | 0.2/0.2 0.2/0.2 2/2 | 0.4/0.4 0.4/0.4 5/5    | 0.4/0.4 0.4/0.4 4/4    | 0.2/0.2 0.2/0.2 4/4   |                     |

The next table is about programming the flash memory of JTAG targets. Here, the picture is completely different.

| MCU                              | SNAP                | PICkit4           | Atmel-ICE           | Power Debugger        | JTAGICE3              | XPLAINED Pro 324PB  |
| -------------------------------- | ------------------- | ----------------- | ------------------- | --------------------- | --------------------- | ------------------- |
| mega324PB<br>mega128<br>mega2560 | 6/3<br/>3/2<br/>7/7 | 5/2<br>2/2<br>5/5 | 8/5<br>5/3<br>10/10 | 8/5<br/>5/3<br/>10/10 | 7/4<br>4/3<br>9/9     | 8/5<br>5/3<br>10/10 |
| mega32u4                         | 5/3<br>3/2<br>7/7   | 4/2<br>2/1<br>5/5 | 6/4<br>4/3<br>10/10 | 7/4<br>4/3<br>10/10   | 6/4<br>4/3<br>9/9<br> |                     |

