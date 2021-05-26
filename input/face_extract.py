import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import face_recognition


def cascade_extract(frame, classifier_a, classifier_b=None):
    """Given a haar_cascade_classifier, returns a list of BB-coordinates of each face in an image.

    Args:
        frame (np.array): image to search for faces in.
        classifier_a (cv.CascadeClassifier): classifier.
        classifier_b (cv.CascadeClassifier, optional): second classifier incase the first one finds no faces.

    Returns:
        tuple: list of n lists as [top, right, bottom, left] for n found faces.

    """
    frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    frame_gray = cv.equalizeHist(frame_gray)

    faces = classifier_a.detectMultiScale(frame_gray)
    if len(faces) == 0 and classifier_b is not None:
        faces = classifier_b.detectMultiScale(frame_gray)
    # OpenCVs coordinates are like numpys
    for i, (x, y, w, h) in enumerate(faces):
        bot = y + w
        top = y
        left = x
        right = x + h
        faces[i] = (top, right, bot, left)

    return faces


def get_cascade_models(face_cascade_path="models/haarcascade_frontalface_alt.xml",
                       face_cascade2_path="models/haarcascade_frontalface_alt2.xml"):
    """Returns 2 classifiers for automatic face detection.

    Args:
        face_cascade_path (str, optional): Path to first model xml.
        Defaults to "models/haarcascade_frontalface_alt.xml".
        face_cascade2_path (str, optional): Path to second model xml.
        Defaults to "models/haarcascade_frontalface_alt2.xml".

    Returns:
        tuple: 2 cv.CascadeClassifier
    """
    face_cascade = cv.CascadeClassifier()
    face_cascade2 = cv.CascadeClassifier()
    if not face_cascade.load(cv.samples.findFile(face_cascade_path)):
        print("--(!)Error loading face cascade")
        exit(0)
    if not face_cascade2.load(cv.samples.findFile(face_cascade2_path)):
        print("--(!)Error loading eyes cascade")
        exit(0)

    return face_cascade, face_cascade2


def face_recog_extract(img):
    """Returns a list of BB-coordinates of each face in an image.

    Args:
        img (np.array): image to search for faces in.

    Returns:
        tuple: list of n lists as [top, right, bottom, left] for n found faces.
    """
    face_locations = face_recognition.face_locations(img)

    return face_locations


def viz_faces(img, face_locations):
    plt.imshow(img)
    for (top, right, bot, left) in face_locations:
        plt.plot(right, bot, 'bo')
        plt.plot(right, top, 'bo')
        plt.plot(left, top, 'bo')
        plt.plot(left, bot, 'bo')
    plt.show()


if __name__ == "__main__":
    imgs = ["data/zoom_ui.jpg", "data/hard_face0.jpg",
            "data/hard_face1.jpg", "data/hard_face2.jpg"]
    # clas1, clas2 = get_cascade_models()
    for img in imgs:
        img = cv.imread(img)
        faces = face_recog_extract(img)
        # cascade_extract(cv.imread(img), clas1, clas2)
        viz_faces(img, faces)
