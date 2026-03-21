import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import urllib.request
import os

# Download model if not present
MODEL_PATH = "hand_landmarker.task"
if not os.path.exists(MODEL_PATH):
    print("Downloading hand landmark model...")
    urllib.request.urlretrieve(
        "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task",
        MODEL_PATH
    )
    print("Done.")

# Finger tip and pip landmark indices
FINGER_TIPS = [8, 12, 16, 20]
THUMB_TIP   = 4

# Setup
base_options  = python.BaseOptions(model_asset_path=MODEL_PATH)
options       = vision.HandLandmarkerOptions(
                    base_options=base_options,
                    num_hands=1,
                    min_hand_detection_confidence=0.5,
                    min_tracking_confidence=0.5)
detector      = vision.HandLandmarker.create_from_options(options)

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w = frame.shape[:2]

    # Convert to MediaPipe image
    rgb        = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image   = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
    result     = detector.detect(mp_image)

    finger_count = 0

    if result.hand_landmarks:
        lm = result.hand_landmarks[0]

        # Thumb: compare x position
        if lm[THUMB_TIP].x < lm[THUMB_TIP - 1].x:
            finger_count += 1

        # Other 4 fingers: tip y above pip y = finger up
        for tip in FINGER_TIPS:
            if lm[tip].y < lm[tip - 2].y:
                finger_count += 1

        # Draw landmarks manually
        for point in lm:
            cx, cy = int(point.x * w), int(point.y * h)
            cv2.circle(frame, (cx, cy), 5, (0, 220, 120), -1)

    cv2.putText(frame, f'Fingers: {finger_count}', (10, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 220, 120), 3)

    cv2.imshow("Finger Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()