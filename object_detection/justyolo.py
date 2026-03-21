"run these commands before running the script"
"python -m venv env"
"source env/Scripts/activate"
"pip install ultralytics" 


from ultralytics import YOLO

model = YOLO('yolov8n.pt')  # downloads automatically on first run
results = model(source=0, show=True)  # 0 = your webcam