//#define LED 23
//#define LED SCK
//#define LED 4
#define LED LED_BUILTIN
byte thisByte = 0;
void setup() {
  pinMode(LED, OUTPUT);
}

void loop() {
  int i=digitalRead(1)+20;
  digitalWrite(LED, HIGH);  
  delay(1000); 
  thisByte = thisByte + i;
  digitalWrite(LED, LOW);      
  thisByte = thisByte + i + 1;
  i = i*5;
  thisByte = thisByte - 3;
  delay(100+thisByte);
}
