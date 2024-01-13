import cv2
import numpy as np
import pytesseract

# Load Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Adjust the path as needed

# Load YOLO
net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
layer_names = net.getUnconnectedOutLayersNames()

# Load image
image = cv2.imread("Nagpur.jpg")
image = cv2.resize(image, (650,750))
height, width, _ = image.shape

# Prepare image for YOLO
blob = cv2.dnn.blobFromImage(image, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
net.setInput(blob)
outs = net.forward(layer_names)

# Get information about detected objects
class_ids = []
confidences = []
boxes = []

for out in outs:
    for detection in out:
        scores = detection[5:]
        class_id = np.argmax(scores)
        confidence = scores[class_id]
        if confidence > 0.5 and class_id == 2:  # Class ID 2 corresponds to cars in COCO dataset
            center_x = int(detection[0] * width)
            center_y = int(detection[1] * height)
            w = int(detection[2] * width)
            h = int(detection[3] * height)

            x = int(center_x - w / 2)
            y = int(center_y - h / 2)

            boxes.append([x, y, w, h])
            confidences.append(float(confidence))
            class_ids.append(class_id)

# Apply non-maximum suppression to remove overlapping bounding boxes
indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

# Extract the region of interest (ROI) containing the license plate
for i in range(len(boxes)):
    if i in indices:
        x, y, w, h = boxes[i]

        # Expand the region to include a bit above and below the car
        roi_y1 = max(0, y - int(0.2 * h))
        roi_y2 = min(height, y + h + int(0.2 * h))

        roi = image[roi_y1:roi_y2, x:x + w]

        # Perform OCR on the license plate region
        license_plate_text = pytesseract.image_to_string(roi, config='--psm 8 --oem 3')

        # Display the license plate number
        print('License Plate Number:', license_plate_text)

        # Display the result
        
        cv2.imshow("License Plate Detection", roi)
        cv2.waitKey(0)
        cv2.destroyAllWindows()



    