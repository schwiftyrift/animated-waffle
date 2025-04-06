import torch
import cv2
from ultralytics import YOLO
import numpy as np
from pathlib import Path

class Detector():
    
    def __init__(self, model_path="best.pt", device=None):
        self.device = device if device else ("cuda" if torch.cuda.is_available() else "cpu")
        print(f"Using device: {self.device}")
        
        self.model = YOLO(str(model_path)).to(self.device)

    def detectObject(self, frame):
        labels = []
        boxes = []

        frameCopy = frame.copy()
        results = self.model(frame)[0]

        for box in results.boxes:
            coords = box.xyxy[0].tolist()  # Extract coordinates as a list
            if len(coords) == 4:  # Ensure there are 4 coordinates
                x1, y1, x2, y2 = map(int, coords)
                conf = float(box.conf[0])
                label_id = int(box.cls[0])
                label = self.model.names[label_id]

                if conf > 0.4:
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, label, (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)

                    labels.append(label)
                    boxes.append((x1, y1, x2, y2))  # Store bounding box as tuple
        
        self.takePhoto(frameCopy, boxes)

        return frame, labels, boxes

    def detectColor(self, frame, boxes):
        """
        Detects the dominant color for multiple bounding boxes, combining both red ranges.
        """
        colors = []

        for box in boxes:
            if len(box) == 4:  # Ensure valid bounding box
                x1, y1, x2, y2 = box
                object_region = frame[y1:y2, x1:x2]

                if object_region.size == 0:
                    colors.append("Unknown")
                    continue

                hsv_object = cv2.cvtColor(object_region, cv2.COLOR_BGR2HSV)

                # HSV color ranges
                color_ranges = {
                    "Red": [([0, 100, 100], [10, 255, 255]),    # Red range 1
                            ([170, 100, 100], [180, 255, 255])],  # Red range 2
                    "Green": ([35, 40, 40], [85, 255, 255]),
                    "Blue": ([94, 80, 2], [126, 255, 255]),
                    "Yellow": ([22, 93, 100], [35, 255, 255]),
                    "Orange": ([10, 100, 100], [25, 255, 255]),
                    "Purple": ([125, 40, 40], [155, 255, 255]),
                    "Pink": ([140, 50, 50], [170, 255, 255]),
                    "Brown": ([10, 40, 20], [30, 255, 200]),
                    "Gray": ([0, 0, 50], [180, 20, 200]),
                    "Black": ([0, 0, 0], [180, 255, 50]),
                    "White": ([0, 0, 200], [180, 30, 255])
                }

                max_coverage = 0
                dominant_color = "Unknown"

                for color, ranges in color_ranges.items():
                    mask = np.zeros(hsv_object.shape[:2], dtype=np.uint8)

                    if isinstance(ranges[0][0], list):  # Multi-range colors like Red
                        for lower, upper in ranges:
                            lower = np.array(lower, dtype=np.uint8)
                            upper = np.array(upper, dtype=np.uint8)
                            mask |= cv2.inRange(hsv_object, lower, upper)
                    else:
                        lower, upper = ranges
                        lower = np.array(lower, dtype=np.uint8)
                        upper = np.array(upper, dtype=np.uint8)
                        mask = cv2.inRange(hsv_object, lower, upper)

                    coverage = (cv2.countNonZero(mask) / mask.size) * 100

                    if coverage > max_coverage and coverage > 5:  # Only consider >5% coverage
                        max_coverage = coverage
                        dominant_color = color

                colors.append(dominant_color)

        return colors
    
    def takePhoto(self, frame, boxes):
        for box in boxes:
            if len(box) == 4:  # Ensure valid bounding box
                x1, y1, x2, y2 = box
                croppedFrame = frame[y1:y2, x1:x2]
                cv2.imwrite("photo.jpg", croppedFrame)    
        return