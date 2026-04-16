from ultralytics import YOLO

model = YOLO("yolov8x-world.pt")

def detect_objects(image, item_list):
    model.set_classes(item_list)
    results = model(image)

    detections = results[0]
    counts = {}

    for cls in detections.boxes.cls:
        label = detections.names[int(cls)]
        counts[label] = counts.get(label, 0) + 1

    return counts, results