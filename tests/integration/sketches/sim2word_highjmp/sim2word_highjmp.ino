// This sketch tests the ability to simulate two word jump/call instructions
// in the upper half of a 256 kB flash memory.

int value[10];

#if FLASHEND > 262142UL
#define cell8 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF
#define cell64 cell8, cell8, cell8, cell8, cell8, cell8, cell8, cell8
#define cell512 cell64, cell64, cell64, cell64, cell64, cell64, cell64, cell64
#define cell4096 cell512, cell512, cell512, cell512, cell512, cell512, cell512, cell512
#define cell16384 cell4096, cell4096, cell4096, cell4096
byte big1[16384] __attribute__((section(".progmem"))) = { cell16384 };
byte big2[16384] __attribute__((section(".progmem"))) = { cell16384 };
byte big3[16384] __attribute__((section(".progmem"))) = { cell16384 };
byte big4[16384] __attribute__((section(".progmem"))) = { cell16384 };
byte big5[16384] __attribute__((section(".progmem"))) = { cell16384 };
byte big6[16384] __attribute__((section(".progmem"))) = { cell16384 };
byte big7[16384] __attribute__((section(".progmem"))) = { cell16384 };
byte big8[16384] __attribute__((section(".progmem"))) = { cell16384 };
byte big9[16384] __attribute__((section(".progmem"))) = { cell16384 };
#endif

int compute_avg()
{
  long result = 0;
  for (int i=0; i < 10; i++) {
    result += value[i];
  }
  return result/10;
}

void setup()
{
  randomSeed(1234);
  Serial.begin(38400);
#if FLASHEND > 262142UL
  Serial.println(pgm_get_far_address(big1));
  Serial.println(pgm_get_far_address(big2));
  Serial.println(pgm_get_far_address(big3));
  Serial.println(pgm_get_far_address(big4));
  Serial.println(pgm_get_far_address(big5));
  Serial.println(pgm_get_far_address(big6));
  Serial.println(pgm_get_far_address(big7));
  Serial.println(pgm_get_far_address(big8));
  Serial.println(pgm_get_far_address(big9));
#endif
}

void loop () {
  int avg;
  long val;
  for (int i = 0; i < 10; i++) {
    val = random();
    value[i] = (int)val; // this is, where to put a breakpoint!
  }
  avg = compute_avg();
  Serial.println(avg); // check for result: = -7196
  delay(500);
}


