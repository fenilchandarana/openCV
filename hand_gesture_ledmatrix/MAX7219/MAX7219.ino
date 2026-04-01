#include <MD_MAX72xx.h>
#include <SPI.h>

#define HARDWARE_TYPE MD_MAX72XX::FC16_HW
#define MAX_DEVICES 16
// din 23
#define CS_PIN 15
// clk 18

// Total grid: 32 wide (4 modules × 8), 8 tall
#define TOTAL_COLS 128  // 4 modules × 8 columns
#define TOTAL_ROWS 8

MD_MAX72XX mx = MD_MAX72XX(HARDWARE_TYPE, CS_PIN, MAX_DEVICES);

void setPixelByNumber(int pixelNum) {
  mx.clear();

  int index = pixelNum - 1; // 0-based

  // Numbering: left to right, bottom to top
  // Row 0 = bottom, Row 7 = top
  int col = index % TOTAL_COLS;         // 0-31, left to right
  int row = TOTAL_ROWS - 1 - (index / TOTAL_COLS);         // 0 = bottom row, goes up

  mx.setPoint(row, col, true);
}

void setup() {
  Serial.begin(9600);
  mx.begin();
  mx.clear();
  Serial.println("Enter pixel number (1-1024):");
}

void loop() {
  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n');
    input.trim();
    int pixelNum = input.toInt();

    int maxPixels = TOTAL_COLS * TOTAL_ROWS; // 1024

    if (pixelNum >= 1 && pixelNum <= maxPixels) {
      setPixelByNumber(pixelNum);
      Serial.print("Pixel ");
      Serial.print(pixelNum);
      Serial.println(" ON");
    } else {
      Serial.println("Invalid! Enter 1 to 1024.");
    }
  }
}
