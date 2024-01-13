import cv2
import requests
import numpy as np
import easyocr

# URL of the IP Webcam video stream on your mobile device
ip_webcam_url = "http://192.168.110.70:8080/video"  # Replace with your mobile device's IP address
# ip_webcam_url = "http://[2409:40c2:2b:916:ec2c:26ff:febc:1f2b]:8080/video"


# Load YOLO model and classes
net = cv2.dnn.readNet("yolov4.weights", "yolov4.cfg")
with open("coco.names", "r") as f:
    classes = f.read().strip().split("\n")

# Get output layer names from YOLO model
output_layers = net.getUnconnectedOutLayersNames()

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'])

# Initialize the stream variable
stream = None

try:
    # Open a connection to the IP Webcam video stream
    stream = requests.get(ip_webcam_url, stream=True)
    bytes_data = bytes()

    # Read and detect vehicles in the video stream in real-time
    while True:
        bytes_data += stream.raw.read(1024)
        a = bytes_data.find(b'\xff\xd8')
        b = bytes_data.find(b'\xff\xd9')
        if a != -1 and b != -1:
            jpg = bytes_data[a:b + 2]
            bytes_data = bytes_data[b + 2:]
            frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)

            # Detect vehicles in the frame using YOLO
            height, width, channels = frame.shape
            blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
            net.setInput(blob)
            outs = net.forward(output_layers)

            class_ids = []
            confidences = []
            boxes = []

            # Extract information about detected vehicles
            for out in outs:
                for detection in out:
                    scores = detection[5:]
                    class_id = np.argmax(scores)
                    confidence = scores[class_id]
                    if confidence > 0.5 and class_id == 2:  # Class ID 2 corresponds to vehicles in COCO dataset
                        center_x = int(detection[0] * width)
                        center_y = int(detection[1] * height)
                        w = int(detection[2] * width)
                        h = int(detection[3] * height)

                        # Rectangle coordinates
                        x = int(center_x - w / 2)
                        y = int(center_y - h / 2)

                        boxes.append([x, y, w, h])
                        confidences.append(float(confidence))
                        class_ids.append(class_id)

            # Non-maximum suppression to remove duplicate boxes
            indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

            # Draw bounding boxes around detected vehicles and recognize license plates
            for i in range(len(boxes)):
                if i in indexes:
                    x, y, w, h = boxes[i]
                    label = str(classes[class_ids[i]])
                    color = (0, 165, 255)  # Orange color in BGR
                    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)

                    # Recognize license plates using EasyOCR
                    plate_roi = frame[y:y + h, x:x + w]
                    plate_text = reader.readtext(plate_roi)

                    if plate_text:
                        recognized_text = plate_text[0][1]
                        # Overlay the recognized license plate number in red text
                        cv2.putText(frame, recognized_text, (x, y - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

            # Display the frame with vehicle bounding boxes and recognized license plates
            cv2.imshow("Vehicle Detection", frame)

            # Press 'q' to quit the video stream
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
except Exception as e:
    print("Error:", e)

finally:
    # Release the video stream and close all windows
    if stream is not None:
        stream.close()
    cv2.destroyAllWindows()