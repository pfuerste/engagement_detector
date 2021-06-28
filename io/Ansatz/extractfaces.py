import face_recognition
import os
from PIL import Image

imagePath = r"E:\Users\Alexander\Desktop\Bilder\testung.png"
os.chdir(r'E:\Users\Alexander\Desktop\Bilder\temp')

image = face_recognition.load_image_file(imagePath)
face_locations = face_recognition.face_locations(image)

x = 0

for face_location in face_locations:
    top, right, bottom, left = face_location

    face_image = image[top:bottom, left:right]
    pil_image = Image.fromarray(face_image)
    pil_image.save(str(x) + '.jpg')
    x = x + 1
