import cv2
import sys
import os

imagePath = r"E:\Users\Alexander\Desktop\Bilder\testung.png"
os.chdir(r'E:\Users\Alexander\Desktop\Bilder\temp')

image = cv2.imread(imagePath)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
faces = faceCascade.detectMultiScale(
    gray,
    scaleFactor=1.1,
    minNeighbors=8,
    minSize=(20, 20)
)

for (x, y, w, h) in faces:
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    roi_color = image[y:y + h, x:x + w]
    cv2.imwrite(str(x)+'x' + str(y)+'y' + '_faces.jpg', roi_color)

status = cv2.imwrite('faces_detected.jpg', image)