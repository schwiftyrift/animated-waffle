import cv2
from detector import Detector
#from database import inputData
import logging

def main ():

    # Suppress YOLOv8 logs
    logging.getLogger("ultralytics").setLevel(logging.CRITICAL)

    label = []

    #Initializes the detector
    detector = Detector(model_path= "yolov8n.pt")

    #Open webcam (Default is 0, other webcam is 1)
    capture = cv2.VideoCapture(0)

    if not capture.isOpened():
        print("Error: Could not open webcam.")
        return

    while capture.isOpened():
        ret, frame = capture.read()

        if not ret:
            print("Failed to grab frame.")
            break
        
        frame, labels = detector.detectObject(frame)

        cv2.imshow("Lost and Found Detection", frame)

        if labels:
            while(len(label) < 20 ):
                label.append(labels)
                print(label)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    capture.release()
    cv2.destroyAllWindows()

    return

if __name__ == "__main__":
    main()

