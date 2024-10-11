#include <Mouse.h>

void setup() {
  // Start serial communication at the same baud rate as the Python script
  Serial.begin(9600);

  // Start the mouse control
  Mouse.begin();
}

void loop() {
  // Check if data is available on the serial port
  if (Serial.available() > 0) {
    // Read the incoming serial data
    String data = Serial.readStringUntil('\n');
    
    // Parse the coordinates (x, y)
    int commaIndex = data.indexOf(',');
    int x = data.substring(0, commaIndex).toInt();
    int y = data.substring(commaIndex + 1).toInt();
    
    // Move the mouse to the specified coordinates
    Mouse.move(x, y);
    
    // Optionally, print the coordinates for debugging
    Serial.print("Moving mouse to: ");
    Serial.print(x);
    Serial.print(", ");
    Serial.println(y);
  }
}