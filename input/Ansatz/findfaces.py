import face_recognition
import os

imagePath = r"E:\Users\Alexander\Desktop\Bilder\testung.png"
os.chdir(r'E:\Users\Alexander\Desktop\Bilder\temp')

image=face_recognition.load_image_file(imagePath)
face_locations=face_recognition.face_locations(image)

print(face_locations)

print(f'There are {len(face_locations)}people in this image')