# Run the  following command before running the script
# python -m venv env
# source env/Scripts/activate
# pip install mediapipe==0.10.13 opencv-python pycaw comtypes protobuf==4.25.3 tensorflow==2.13.0
# pip install numpy==1.26.4


import cv2 as cv
import mediapipe as mp

def main():
    cap = cv.VideoCapture(0)
    cap.set(cv.CAP_PROP_FRAME_WIDTH, 960)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, 540)

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

        ret, image = cap.read()
        if not ret:
            break

        image = cv.flip(image, 1)
        rgb = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        results = hands.process(rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                h, w = image.shape[:2]

                # Build point list
                pts = []
                for landmark in hand_landmarks.landmark:
                    x = min(int(landmark.x * w), w - 1)
                    y = min(int(landmark.y * h), h - 1)
                    pts.append((x, y))

                # Connections: (start_index, end_index)
                connections = [
                    # Palm
                    (0,1),(1,2),(2,3),(3,4),       # Thumb
                    (5,6),(6,7),(7,8),        # Index
                    (5,9),(9,10),(10,11),(11,12),   # Middle
                    (9,13),(13,14),(14,15),(15,16), # Ring
                    (13,17),(17,18),(18,19),(19,20),# Pinky
                    (0,17),(2,5),                   # Palm base
                ]

                for a, b in connections:
                    cv.line(image, pts[a], pts[b], (0, 0, 0), 6)
                    cv.line(image, pts[a], pts[b], (255, 255, 255), 2)

                for i, pt in enumerate(pts):
                    cv.circle(image, pt, 6, (255, 255, 255), -1)
                    cv.circle(image, pt, 6, (0, 0, 0), 1)
                    cv.putText(image, str(i), (pt[0] + 8, pt[1] + 4),
                               cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv.LINE_AA)
                    cv.putText(image, str(i), (pt[0] + 8, pt[1] + 4),
                               cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv.LINE_AA)

        cv.imshow('Hand Landmarks', image)

    cap.release()
    cv.destroyAllWindows()

if __name__ == '__main__':
    main()