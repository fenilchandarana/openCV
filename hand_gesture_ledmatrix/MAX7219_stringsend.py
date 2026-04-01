#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cv2 as cv
import numpy as np
import mediapipe as mp
import serial

SERIAL_PORT = 'COM6'
BAUD_RATE = 115200

GRID_SIZE = 32        # 32x32 LED matrix
DOT_RADIUS = 10       # radius of each LED circle
HIT_THRESHOLD = 8     # pixels — how close a line/point needs to be to light up a dot

CONNECTIONS = [
    (0,1),(1,2),(2,3),(3,4),
    (5,6),(6,7),(7,8),
    (5,9),(9,10),(10,11),(11,12),
    (9,13),(13,14),(14,15),(15,16),
    (13,17),(17,18),(18,19),(19,20),
    (0,17),(2,5),
]

def point_to_segment_dist(px, py, ax, ay, bx, by):
    """Distance from point (px,py) to line segment (ax,ay)-(bx,by)."""
    dx, dy = bx - ax, by - ay
    if dx == 0 and dy == 0:
        return np.hypot(px - ax, py - ay)
    t = max(0, min(1, ((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy)))
    return np.hypot(px - (ax + t * dx), py - (ay + t * dy))

def main():
    cap = cv.VideoCapture(0)
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)

    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.5,
    )

    while True:
        key = cv.waitKey(10)
        if key == 27:  # ESC to quit
            break

        ret, frame = cap.read()
        if not ret:
            break

        frame = cv.flip(frame, 1)

        # Crop to square (center crop) ----------------------------------------
        h, w = frame.shape[:2]
        size = min(h, w)
        x0 = (w - size) // 2
        y0 = (h - size) // 2
        frame = frame[y0:y0 + size, x0:x0 + size]

        # Mediapipe detection -------------------------------------------------
        rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        results = hands.process(rgb)

        # Build landmark pixel coords -----------------------------------------
        pts = []
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                for lm in hand_landmarks.landmark:
                    pts.append((int(lm.x * size), int(lm.y * size)))

        # Draw skeleton on camera frame ---------------------------------------
        if pts:
            for a, b in CONNECTIONS:
                cv.line(frame, pts[a], pts[b], (0, 0, 0), 6)
                cv.line(frame, pts[a], pts[b], (255, 255, 255), 2)
            for pt in pts:
                cv.circle(frame, pt, 6, (255, 255, 255), -1)
                cv.circle(frame, pt, 6, (0, 0, 0), 1)

        # Build LED grid overlay ----------------------------------------------
        grid_layer = np.zeros_like(frame)
        spacing = size / GRID_SIZE
        half = int(spacing / 2)
        lit_leds = []  # track which LEDs are on this frame

        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                cx = int(col * spacing + half)
                cy = int(row * spacing + half)
                led_num = row * GRID_SIZE + col + 1

                lit = False
                if pts:
                    for px, py in pts:
                        if np.hypot(cx - px, cy - py) < HIT_THRESHOLD:
                            lit = True
                            break
                    if not lit:
                        for a, b in CONNECTIONS:
                            ax, ay = pts[a]
                            bx, by = pts[b]
                            if point_to_segment_dist(cx, cy, ax, ay, bx, by) < HIT_THRESHOLD:
                                lit = True
                                break

                if lit:
                    lit_leds.append(led_num)
                    cv.circle(grid_layer, (cx, cy), DOT_RADIUS, (0, 255, 80), -1)
                else:
                    cv.circle(grid_layer, (cx, cy), DOT_RADIUS - 2, (80, 80, 80), 1)

        # Print lit LEDs to terminal
        # Send lit LEDs to ESP32
        if lit_leds:
            data = ','.join(str(n) for n in lit_leds) + '\n'
            ser.write(data.encode())
            print(f"Sent: {data.strip()}")
        else:
            ser.write(b'\n')  # send empty line so ESP32 knows to clear

        # Blend grid over camera frame ----------------------------------------
        cv.addWeighted(frame, 1.0, grid_layer, 0.85, 0, frame)

        cv.imshow('LED Matrix Preview', frame)
    ser.close()
    cap.release()
    cv.destroyAllWindows()

if __name__ == '__main__':
    main()