#include <Servo.h>

Servo servo;

void setup() {
  Serial.begin(9600);
  // put your setup code here, to run once:
  servo.attach(5); //D1
  servo.write(0);

  delay(2000);
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available() > 0) {
    char command = Serial.read();
    if (command == '1') {
      servo.write(90);
    } else if (command == '0') {
      servo.write(0);
    }
  }
}
