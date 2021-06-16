import face_recognition
import os
import pickle


def get_face_encodings(face_img):
    """Given an Image with faces in it,
    returns an list with the encodings of all found faces

    Args:
        face_img : image with faces in it

    Return:
        face_encoding : list of 128 dimension face encodings

    """
    face_locations = face_recognition.face_locations(face_img)
    face_encodings = face_recognition.face_encodings(face_img, face_locations)
    return face_encodings


def compare_face_to_others(face_img, encodings_list):
    """Given an Image with faces in it and a list of known faces,
        returns index if the image was found

    Args:
        face_img : image with faces in it
        encodings_list : list of 128 dimension face encodings

    Return:
        match : List of True and false which face is known

    """
    unknown_face_encodings = face_recognition.face_encodings(face_img)
    for unknown_face_encodings in unknown_face_encodings:
        matches = face_recognition.compare_faces(
            encodings_list, unknown_face_encodings)
    return matches


def save_encodings(list_of_face_encodings, lecture_name):
    """Saving the Encodings depending on the current lecture

    Args:
        list_of_face_encodings : list of known encodings
        lecture_name : current lecture name

    pass

    """

    with open('{}.dat'.format(lecture_name), 'xb') as f:
        pickle.dump(list_of_face_encodings, f)
    pass


def load_encodings(lecture_name):
    """Loading the Encodings of a special lecture

    Args:
        lecture_name : name of the wanted lecture

    return:
        known_encodings : list of known encodings

    """

    with open('{}.dat'.format(lecture_name), 'rb') as f:
        face_encodings = pickle.load(f)
    return face_encodings
