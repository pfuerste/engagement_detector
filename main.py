import os
import time
import numpy as np
from face_recognition.api import face_encodings, compare_faces
import yaml
import keras
import face_recognition
from io_utils import encodings_identity as ei
from io_utils import persistence
from io_utils import face_extract as fe
from io_utils.utils import crop_bbs
from io_utils.screen_grab import screenshot
from cnn.models import get_func_model


def main():
    pass
    # read config (developer info)
    root = yaml.safe_load(open("config.yml"))["root"]
    model_path = yaml.safe_load(open("config.yml"))["model"]
    log_dir = yaml.safe_load(open("config.yml"))["logs"]

    # load model
    model = get_func_model()
    model.load_weights(model_path)

    # TODO
    # open gui
    # read from gui:
    # lecture name (new or dropdown of old ones)
    # input method (default: screenshot)
    input_via = screenshot
    # inference intervals (?)


    # TODO ! list of found people with image, encodings and metric instead of many lists
    stop = False
    last_encodings = list()
    # loop while (not stop button pressed)
    #while not stop:
        # get image
    for j in range(5):
        start = time.perf_counter()
        imgs = input_via()
        # find faces
        face_locs = list()
        faces = list()
        encodings = list()
        for img in imgs:
            img = np.array(img)
            locs = fe.face_recog_extract(img)
            face_locs.extend(locs)
            for loc in locs:
                face = crop_bbs(img, [loc])
                faces.append(*face)
        # get encodings
        encode_start = time.perf_counter()

        for face in faces:
            # TODO Does not take coordinates, which would speed it up:
            enc = face_recognition.face_encodings(face)
            #print(len(enc))
            #print(type(enc[0]))

            encodings.append(enc)
        encode_end = time.perf_counter()
        print(f"Encodings took {(encode_end-encode_start)} seconds.")

            #  (0, face.shape[1], face.shape[0], 0)))
        # compare to last encodings
        compare_start = time.perf_counter()
        if last_encodings:
            for encoding in encodings:
                print(len(last_encodings))
                print(len(encoding))
                ret = face_recognition.compare_faces(last_encodings, encoding)
        #    print(ret)
        compare_end = time.perf_counter()
        print(f"Comparaisions took {(compare_end-compare_start)} seconds.")

        last_encodings = encodings
        # inference
        # match encodings & metrics
        # calc intra-session metrics
        # update gui
        end = time.perf_counter()
        print(f"Processing one image (with {len(face_locs)} found persons) took {(end-start)} seconds.")
    # save data


if __name__ == "__main__":
    main()
    # start = time.perf_counter()
    # preds = model.predict(imgs)
    # end = time.perf_counter()
    # print(f"3 images took {end-start} time(s).")
