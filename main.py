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
from cnn.models import get_func_model, batchify


def manage_encodings(person_data, new_inferences, all_encodings, curr_encodings, t):
    # Manage early timesteps
    # Initialize structures in first time step if faces were found
    if t == 0 and curr_encodings:
        print("initializin encoding structures at t==0")
        for i in range(len(new_inferences)):
            person_data.append([[new_inferences[i][0]],
                                [new_inferences[i][1]],
                                [new_inferences[i][2]],
                                [new_inferences[i][3]]])
        all_encodings = curr_encodings
        return person_data, all_encodings

    # No detected faces in the beginnning of the lecture, fill gaps
    if not all_encodings and curr_encodings:
        print("initializin encoding structures at t>0")
        person_data = list()
        diff = t

        for i in range(len(new_inferences)):
            person_data.append([[-1] * diff, [-1] * diff, [-1] * diff, [-1] * diff])
            person_data[i][0].append(new_inferences[i][0])
            person_data[i][1].append(new_inferences[i][1])
            person_data[i][2].append(new_inferences[i][2])
            person_data[i][3].append(new_inferences[i][3])
        all_encodings = curr_encodings
        return person_data, all_encodings

    rets = dict(zip(range(len(all_encodings)+1), [0] * (len(all_encodings)+1)))
    print(rets)
    for encoding in curr_encodings:
        # TODO check this tolerance value, maybe implement adaptive tolerance for hard cases
        ret = face_recognition.compare_faces(all_encodings, encoding, tolerance=0.3)
        ret = [1 if x else 0 for x in ret]
        rets[sum(ret)] += 1

        # Same faces found in earlier iteration
        if sum(ret) == 1:
            person_index = ret.index(1)
            for i in range(4):
                # Saving like this (4 lists of len t per person) is bad memory access,
                # but better for later evaluation
                # TODO fill missing spots in t, TEST -1
                diff = t - len(person_data[person_index][i]) - 1
                person_data[person_index][i].extend([-1] * diff)
                person_data[person_index][i].append(new_inferences[person_index][i])

        # This person is newly recognized
        if sum(ret) == 0:
            all_encodings.append(encoding)

    # print(rets)
    # print(len(curr_encodings) == sum(rets.values()))
    return person_data, all_encodings


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
    lecture = "Test"

    # input method (default: screenshot)
    input_via = screenshot

    # Performance_mode or not
    performance_mode = False

    # TODO while not stop & inference intervals (hardcoden)

    stop = False
    all_encodings = list()
    # 2 Lists for Results, because time is more important than memory
    vis_data = [[], [], [], []]
    person_data = list()
    t = 0
    # loop while (not stop button pressed)
    # while not stop:
    # get image
    # TODO all functions have to work with zero faces too
    for j in range(3):
        start = time.perf_counter()
        imgs = input_via()
        print("screenshot done")
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
                if not performance_mode:
                    if not faces:
                        t += 1
                        continue
                    # Does not find encodings on just face, needs to take whole image
                    enc = face_recognition.face_encodings(img, [loc])
                    curr_encodings.append(enc[0])
        if not faces:
            t += 1
            print("no_faces_detected")
            continue
        # inference
        # Returns array of shape [num_targets=4, num_persons, num_classes=4]
        probs = model.predict(batchify(faces))

        probs = np.array(probs)
        # Reshape to [num_targets=4, num_persons] by taking index of max in last dim
        preds = probs.argmax(axis=2)
        person_preds = preds.T

        # Update visualization data
        for i, emotion in enumerate(preds):
            vis_data[i].append(emotion)

        # match encodings & metrics
        if not performance_mode:
            person_data, all_encodings = manage_encodings(person_data, person_preds, all_encodings, curr_encodings, t)
            # print(person_data)
        # calc intra-session metrics
        # update gui
        print(person_data)
        t += 1
        end = time.perf_counter()
        print(f"Processing one image (with {len(face_locs)} found persons) took {(end-start)} seconds.")
    # save data


if __name__ == "__main__":
    main()
    # start = time.perf_counter()
    # probs = model.predict(imgs)
    # end = time.perf_counter()
    # print(f"3 images took {end-start} time(s).")
