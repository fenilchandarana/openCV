from ultralytics import YOLO

model = YOLO(r'D:\docs\openCV\object_detection\runs\detect\train4\weights\best.pt') # <-- paste your path here. Keep the prefix r
results = model(source=0, show=True)