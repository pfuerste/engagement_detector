import face_recognition as fr
import numpy as np
import cv2
import os
import face_recognition
from time import sleep
imagePath = r"E:\Users\Alexander\Desktop\Bilder\testung.png"
os.chdir(r'E:\Users\Alexander\Desktop\Bilder\temp')


# TODO Rechtschreibfehler, so läufts nicht
# TODO Docstrings, siehe readme oder mein Code
# TODO paths aus config.yml lesen, siehe andere Ordner
# TODO Ordner (z.B.) /faces aus yml lesen (root/data/faces?), das sollte nicht einfach in cwd sein
# TODO /faces dort generieren falls nicht schon da (os.mkdir)
# TODO visualisierung rausnehmen oder optional machen, brauch man später nicht mehr
# TODO Weitere Modularisierung: encoding sollten in einer Funktion im  Speicher gehalten werden, damit währrend einer
# Vorlesung nicht dauernd Files gelesen & geschrieben werden müssen. Nach
# der Vorlesung werden alle encodings gespeichert um bei der nächsten VL
# zu vergleichen wer wer ist.
# TODO die anderen Dateien löschen?


def get_encoded_faces():
    encoded = {}
    for dirpath, dnames, fnames in os.walk("./faces"):
        for f in fnames:
            if f.endswith(".jpg") or f.endswith(".png"):
                face = fr.load_image_file("faces/" + f)
                encoding = fr.face_encodings(fase)[0]
                encoded[f.split(".")[0]] = encoding

    return encoded


def unknown_image_encoded(img):
    face = fr.load_image_file("temp/" + img)
    encoding = fr.face_encodings(face)[0]
    return encoding


def classify_face(im):
    faces = get_encoded_faces()
    faces_encoded = list(faces.values())
    known_face_names = list(faces.keys())

    img = cv2.imread(im, 1)
    face_locations = face_recognition.face_locations(img)
    unknown_face_encodings = face_recognition.face_encodings(
        img, face_locations)

    face_names = []
    for face_encoding in unknown_face_encodings:
        matches = face_recognition.compare_faces(faces_encoded, face_encoding)
        name = "Unknown"

        face_distances = face_recognition.face_distance(
            faces_encoded, face_encoding)
        best_macht_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]

        face_names.append(name)

        for(top, right, bottom, left), name in zip(face_locations, face_names):
            cv.rectangle(img, (left - 20, top - 20),
                         (right + 20, bottom + 20), (255, 0, 0), 2)

            cv.rectangle(img, (left - 20, top - 20), (right + 20,
                         bottom + 20), (255, 0, 0), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(img, name, (left - 20, bottom + 15),
                        font, 1.0, (255, 255, 255), 2)

    while TRUE:

        cv2.imshow('Video', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            return face_names


print(classify_face(imagePath))
