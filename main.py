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
from io_utils.utils import crop_bbs, batchify
from io_utils.screen_grab import screenshot
from cnn.models import get_func_model


def manage_encodings(inference_data, new_inferences, all_encodings, curr_encodings):
    # Same faces found in current iteration than earlier
    if all_encodings == curr_encodings:
        assert len(new_inferences) == len(inference_data)
        for i, inference in new_inferences:
            inference_data[i].append(inference)


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
    # Performance_mode or not
    input_via = screenshot
    # inference intervals (hardcoden)

    stop = False
    all_encodings = list()
    inference_data = list()
    # loop while (not stop button pressed)
    # while not stop:
    # get image
    for j in range(2):
        start = time.perf_counter()
        imgs = input_via()
        # find faces
        face_locs = list()
        faces = list()
        curr_encodings = list()
        for img in imgs:
            img = np.array(img)
            locs = fe.face_recog_extract(img)
            face_locs.extend(locs)
            # save encodings and faces
            for loc in locs:
                face = crop_bbs(img, [loc])
                faces.append(*face)
                # Does not find encodings on just face, needs to take whole image
                enc = face_recognition.face_encodings(img, [loc])
                curr_encodings.append(enc[0])

        # inference
        # Returns array of shape [num_targets=4, num_persons, num_classes=4]
        probs = model.predict(batchify(faces))
        probs = np.array(probs)
        # Reshape to [num_targets=4, num_persons] by taking index of max in last dim
        preds = probs.argmax(axis=2)
        person_scores = preds.T

        # probs = np.squeeze(probs, axis=-1)
        # print(probs.shape)
        # print(probs[0])
        # print(probs[0, 0])
        # print(probs[1, 0])

        # probs_person = probs.T  # np.reshape(probs, (probs.))
        # print(probs_person)
        break
        # match encodings & metrics
        compare_start = time.perf_counter()
        if all_encodings:
            for encoding in curr_encodings:
                ret = face_recognition.compare_faces(all_encodings, encoding)
                ret = [1 if x else 0 for x in ret]
                # if sum(ret) == 1:

        compare_end = time.perf_counter()
        print(f"Comparisions took {(compare_end-compare_start)} seconds.")
        # Update data-structures
        all_encodings = curr_encodings
        # calc intra-session metrics
        # update gui
        end = time.perf_counter()
        print(f"Processing one image (with {len(face_locs)} found persons) took {(end-start)} seconds.")
    # save data


if __name__ == "__main__":
    main()
    # start = time.perf_counter()
    # probs = model.predict(imgs)
    # end = time.perf_counter()
    # print(f"3 images took {end-start} time(s).")
