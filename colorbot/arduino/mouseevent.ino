#include <Mouse.h>

void setup() {
  Serial.begin(9600);

  Mouse.begin();
}

void loop() {
  if (Serial.available() > 0) {

    String data = Serial.readStringUntil('\n');
    
    // parse coordinates
    int commaIndex = data.indexOf(',');
    int x = data.substring(0, commaIndex).toInt();
    int y = data.substring(commaIndex + 1).toInt();
    
    // move mouse
    Mouse.move(x, y);
    
    // debugging
    Serial.print("Moving mouse to: ");
    Serial.print(x);
    Serial.print(", ");
    Serial.println(y);
  }
}