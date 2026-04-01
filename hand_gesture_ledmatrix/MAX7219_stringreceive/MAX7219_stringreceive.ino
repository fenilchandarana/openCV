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
  // removed mx.clear() from here
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

    mx.clear();  // clear all LEDs first

    if (input.length() == 0) return;  // empty = clear only

    // Parse comma-separated LED numbers
    int start = 0;
    while (start < input.length()) {
      int comma = input.indexOf(',', start);
      if (comma == -1) comma = input.length();

      int physicalInput = input.substring(start, comma).toInt();

      // Look up and set each LED
      for (int i = 0; i < MAPPING_SIZE; i++) {
        if (physical[i] == physicalInput) {
          setPixelByNumber(electrical[i]);
          break;
        }
      }

      start = comma + 1;
    }
  }
}
