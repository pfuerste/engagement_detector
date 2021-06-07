import face_recognition
from PIL import Image, ImageDraw
import os

os.chdir(r'E:\Users\Alexander\Desktop\Bilder')
imagePath = r"E:\Users\Alexander\Desktop\Bilder\testung.png"

image_of_null =face_recognition.load_image_file('./temp/0.jpg')
null_face_encoding=face_recognition.face_encodings(image_of_null)[0]

image_of_eins =face_recognition.load_image_file('./temp/1.jpg')
eins_face_encoding=face_recognition.face_encodings(image_of_eins)[0]

image_of_zwei =face_recognition.load_image_file('./temp/2.jpg')
zwei_face_encoding=face_recognition.face_encodings(image_of_zwei)[0]

known_face_encodings=[
    null_face_encoding,
    eins_face_encoding,
    zwei_face_encoding]

known_face_names=[
    "null",
    "eins",
    "zwei"]

test_image=face_recognition.load_image_file(imagePath)

face_locations=face_recognition.face_locations(test_image)
face_encodings=face_recognition.face_encodings(test_image,face_locations)

pil_image=Image.fromarray(test_image)

draw=ImageDraw.Draw(pil_image)

for(top,right,bottom,left),face_encoding in zip(face_locations,face_encodings):
    matches=face_recognition.compare_faces(known_face_encodings,face_encoding,tolerance=0.5)

    name="Unknown Person"

    if True in matches:
        first_match_index=matches.index(True)
        name=known_face_names[first_match_index]

    draw.rectangle(((left,top),(right,bottom)),outline=(255,255,255))
    text_width,text_height=draw.textsize(name)
    draw.rectangle(((left,bottom-text_height-10),(right,bottom)),fill=(0,0,0),outline=(0,0,0))
    draw.text((left+6,bottom-text_height-5),name,fill=(255,255,255,255))

del draw

pil_image.show()
