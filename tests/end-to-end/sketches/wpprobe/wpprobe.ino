// Watchpoint probe for the e2e tests watch_hw and watch_none: one variable only written,
// one only read, and a 2-byte one (read, then written)
volatile uint8_t probe_w;
volatile uint8_t probe_r = 7;
volatile uint8_t sink;
volatile uint16_t probe_w16;
void setup() {}
void loop() {
  for (uint16_t i = 0; i < 1000; i++) { sink = i; }   // a stretch without the probes
  probe_w++;
  sink = probe_r;
  probe_w16 += 3;
}
