// Flash fill test. Almost all the flash memory is filled and then tested.
// If successful, the LED will be on (SCK and LED_BUILTIN).
// If unsuccessful, the LED blinks fast.
// In addition, a message is printed (for MCUs with more than 2kB)

#define LED0 SCK
#ifdef LED_BUILTIN
#define LED1 LED_BUILTIN
#else
#define LED1 LED0
#endif

#include <progmem_far.h>
#include <avr/pgmspace.h>

#define SEQ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255

#define SEQ1K SEQ, SEQ, SEQ, SEQ
#define SEQ2K SEQ1K, SEQ1K
#define SEQ4K SEQ2K, SEQ2K
#define SEQ5K SEQ4K, SEQ1K
#define SEQ6K SEQ4K, SEQ2K
#define SEQ8K SEQ4K, SEQ4K
#define SEQ12K SEQ8K, SEQ4K
#define SEQ14K SEQ8K, SEQ6K
#define SEQ16K SEQ8K, SEQ8K
#define SEQ28K SEQ14K, SEQ14K
#define SEQ30K SEQ16K, SEQ14K
#define SEQ31K SEQ30K, SEQ1K
#define SEQ32K SEQ31K, SEQ, SEQ, SEQ

#if FLASHEND < 16384UL
    #define TABNUM 1
    const byte PROGMEM tab0[] = { 37,
    #if FLASHEND < 1024UL
                        SEQ,
    #elif FLASHEND < 2048UL
                        SEQ, SEQ, SEQ,
    #elif FLASHEND < 4096UL
                        SEQ1K, SEQ, SEQ,
    #elif FLASHEND < 8192UL
                        SEQ5K, SEQ, SEQ,
    #else
                        SEQ12K, SEQ, SEQ,
    #endif
                            69 };
#else
    #if FLASHEND > 262142UL
      #define TABNUM 8
      const byte PROGMEM_FAR tab7[] = {37, SEQ32K, 69};
      const byte PROGMEM_FAR tab6[] = {37, SEQ32K, 69};
      const byte PROGMEM_FAR tab5[] = {37, SEQ32K, 69};
      const byte PROGMEM_FAR tab4[] = {37, SEQ32K, 69};
    #endif
    #if FLASHEND > 131070UL
      #ifndef TABNUM
          #define TABNUM 4
      #endif
      const byte PROGMEM_FAR tab3[] = {37, SEQ32K, 69};
      const byte PROGMEM_FAR tab2[] = {37, SEQ32K, 69};
    #endif
    #if FLASHEND > 65534UL
      #ifndef TABNUM
          #define TABNUM 2
      #endif
      const byte PROGMEM_FAR tab1[] = {37, SEQ31K, 69};
    #endif
    #ifndef TABNUM
        #define TABNUM 1
    #endif
    const byte PROGMEM tab0[] = {37, SEQ28K, 69};
#endif

bool OK = true;

byte pgm_read_byte_near_or_far(unsigned long addr)
{
#ifdef __ELPM
    return pgm_read_byte_far(addr);
#else
    return pgm_read_byte_near((unsigned int)addr);
#endif
}

void flashOK()
{
  digitalWrite(LED0, HIGH);
  digitalWrite(LED1, HIGH);
#if FLASHEND > 2048
  Serial.println(F("\nTest succeeded"));
#endif
  exit(0);
}

void flashError()
{
  digitalWrite(LED0,LOW);
  digitalWrite(LED1,LOW);
#if FLASHEND > 2048
        Serial.println(F("Test failed"));
#endif
}

bool checktab(unsigned long tab, int count)
{
    if (pgm_read_byte_near_or_far(tab++) != 37) return false;
    count--;
    while (pgm_read_byte_near_or_far(tab) != 69) {
        for (int i = 0; i < 256; i++)
        {
            count--;
            if (pgm_read_byte_near_or_far(tab++) != i or count < 0) {
                return false;
            }
        }
    }
    count--;
    return (count == 0);
}

void setup ()
{
#if FLASHEND > 2048
    Serial.begin(19200);
    Serial.println(F("Flash fill test"));
#endif
    pinMode(LED0, OUTPUT);
    pinMode(LED1, OUTPUT);
    unsigned long addr[TABNUM] = {
        pgm_get_far_address(tab0),
        #if TABNUM >= 2
        pgm_get_far_address(tab1),
        #endif
        #if TABNUM >= 4
        pgm_get_far_address(tab2),
        pgm_get_far_address(tab3),
        #endif
        #if TABNUM >= 8
        pgm_get_far_address(tab4),
        pgm_get_far_address(tab5),
        pgm_get_far_address(tab6),
        pgm_get_far_address(tab7),
        #endif
    };
    unsigned int length[TABNUM] = {
        sizeof(tab0),
        #if TABNUM >= 2
        sizeof(tab1),
        #endif
        #if TABNUM >= 4
        sizeof(tab2),
        sizeof(tab3),
        #endif
        #if TABNUM >= 8
        sizeof(tab4),
        sizeof(tab5),
        sizeof(tab6),
        sizeof(tab7),
        #endif
    };

    for (int i=0; i < TABNUM; i++) {
        //Serial.print(".");
        if (!checktab(addr[i], length[i])) {
            OK = false;
        }
    }
    if (OK) {
      flashOK();
    } else {
      flashError();
    }
}

void loop ()
{
    digitalWrite(LED0, HIGH);
    digitalWrite(LED1, HIGH);
    delay(200);
    digitalWrite(LED0, LOW);
    digitalWrite(LED1, LOW);
    delay(200);
}

