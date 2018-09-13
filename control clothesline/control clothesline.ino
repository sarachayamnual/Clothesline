void setup() {
  Serial.begin(9600);
  pinMode(9, OUTPUT);
  pinMode(8, OUTPUT);
}
int readstate = 0;
void loop() {
  readstate = Serial.read(), "0" ;
  if (readstate == 48) {
    // 48 = 0
    clotheslineOff();
  }
  else if (readstate == 49){
    // 49 = 1
    clotheslineOn();
  } 
} 
 
void clotheslineOff() {  
    digitalWrite(8, HIGH);
    delay(1000);
    digitalWrite(9, LOW);
    delay(1000);
   
}
void clotheslineOn() {
    digitalWrite(9, HIGH);
    delay(1000);
    digitalWrite(8, LOW);
    delay(1000);
}


