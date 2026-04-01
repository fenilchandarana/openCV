#include "mapping.h"

void setup() {
  Serial.begin(115200);
  Serial.println("Ready. Enter a physical value:");
}

void loop() {
  if (Serial.available()) {
    int input = Serial.parseInt();

    if (Serial.available()) {
      while (Serial.available()) Serial.read(); // flush
    }

    // Linear search — simple and works for any ordering
    bool found = false;
    for (int i = 0; i < MAPPING_SIZE; i++) {
      if (physical[i] == input) {
        Serial.println(electrical[i]);
        found = true;
        break;
      }
    }

    if (!found) {
      Serial.print("No match found for: ");
      Serial.println(input);
    }
  }
}
