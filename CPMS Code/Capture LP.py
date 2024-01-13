'''Code for realtime'''
# import cv2
# import numpy as np

# frameWidth = 640    #Frame Width
# frameHeight = 480   # Frame Height

# plateCascade = cv2.CascadeClassifier('haarcascade_russian_plate_number.xml')
# minArea = 500


# cap =cv2.VideoCapture(0)
# cap.set(3,frameWidth)
# cap.set(4,frameHeight)
# cap.set(10,150)
# count = 0

# while True:
#     success , img  = cap.read()

#     imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#     numberPlates = plateCascade.detectMultiScale(imgGray, 1.1, 4)

#     for (x, y, w, h) in numberPlates:
#         area = w*h
#         if area > minArea:
#             cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
#             cv2.putText(img,"NumberPlate",(x,y-5),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)
#             imgRoi = img[y:y+h,x:x+w]
#             cv2.imshow("ROI",imgRoi)
#     cv2.imshow("Result",img)
#     if cv2.waitKey(1) & 0xFF == ord('s'):
#         cv2.imwrite("Number\\Images\\Numberplate"+str(count)+'.jpg',imgRoi)
#         cv2.rectangle(img,(0,200),(640,300),(0,255,0),cv2.FILLED)
#         cv2.putText(img,"Scan Saved",(15,265),cv2.FONT_HERSHEY_COMPLEX,2,(0,0,255),2)
#         cv2.imshow("Result",img)
#         cv2.waitKey(500)
#         count+=1
'''Code for images'''
import cv2

frameWidth = 640    # Frame Width
frameHeight = 480   # Frame Height

plateCascade = cv2.CascadeClassifier('haarcascade_russian_plate_number.xml')
minArea = 500

# Load an image
img = cv2.imread('Output\car1.jpg')

imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

numberPlates = plateCascade.detectMultiScale(imgGray, 1.1, 4)

for (x, y, w, h) in numberPlates:
    area = w * h
    if area > minArea:
        # Extend the cropping region to include the area above the number plate
        y_start = max(0, y - int(h * 0.2))  # Adjust the value (0.2) as needed
        imgRoi = img[y_start:y + h, x:x + w]

        # Zoom in on the number plate (adjust the factor as needed)
        zoom_factor = 2  # You can adjust this value for more or less zoom
        imgZoomed = cv2.resize(imgRoi, (int(w * zoom_factor), int(h * zoom_factor)))

# Display the original and zoomed images
cv2.imshow("Original Image", img)
cv2.imshow("Zoomed Number Plate", imgZoomed)
cv2.waitKey(0)
cv2.destroyAllWindows()


