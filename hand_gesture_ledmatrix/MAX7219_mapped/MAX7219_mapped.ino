#include <MD_MAX72xx.h>
#include <SPI.h>
#include "mapping.h"

#define HARDWARE_TYPE MD_MAX72XX::FC16_HW
#define MAX_DEVICES 16
#define CS_PIN 15

#define TOTAL_COLS 128
#define TOTAL_ROWS 8

MD_MAX72XX mx = MD_MAX72XX(HARDWARE_TYPE, CS_PIN, MAX_DEVICES);

void setPixelByNumber(int pixelNum) {
  mx.clear();
  int index = pixelNum - 1;
  int col = index % TOTAL_COLS;
  int row = TOTAL_ROWS - 1 - (index / TOTAL_COLS);
  mx.setPoint(row, col, true);
}

void setup() {
  Serial.begin(115200);
  mx.begin();
  mx.clear();
  Serial.println("Enter physical value:");
}

void loop() {
  if (Serial.available()) {
    String input = Serial.readStringUntil('\n');
    input.trim();
    int physicalInput = input.toInt();

    // Look up electrical value
    bool found = false;
    for (int i = 0; i < MAPPING_SIZE; i++) {
      if (physical[i] == physicalInput) {
        int electricalValue = electrical[i];
        setPixelByNumber(electricalValue);
        Serial.print("Physical ");
        Serial.print(physicalInput);
        Serial.print(" → Electrical ");
        Serial.print(electricalValue);
        Serial.println(" ON");
        found = true;
        break;
      }
    }

    if (!found) {
      Serial.print("No match found for: ");
      Serial.println(physicalInput);
    }
  }
}
