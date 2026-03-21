from ultralytics import YOLO

model = YOLO('yolov8n.pt')

model.train(
    data=r'D:\docs\openCV\object_detection\Multimeter.yolov8\data.yaml',  # <-- paste your path here, keep the r prefix
    epochs=50,
    imgsz=640,
    batch=8
)