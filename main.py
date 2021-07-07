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
import io_utils.screen_grab
from cnn.models import get_func_model, batchify
import gui.plots
import gui.guiRunning
import gui.guiStart


def fill_up_inference_data(inferences, t, index=None):
    for i, single_data in enumerate(inferences):
        if index and i != index:
            # Make this function usable for filling up single persons too
            continue
        filled = len(single_data[0])
        diff = t - filled
        for emotion_data in single_data:
            assert len(emotion_data) == filled
            emotion_data.extend([-1] * diff)
    return inferences


def manage_encodings(person_data, new_inferences, all_encodings, curr_encodings, t):
    # TODO Test for change of positions
    # Manage early timesteps
    # Initialize structures in first time step if faces were found
    if t == 0 and curr_encodings and not all_encodings:
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

    # "Usual" case: Found faces during lecture
    rets = dict(zip(range(len(all_encodings) + 1), [0] * (len(all_encodings) + 1)))
    for preds, encoding in zip(new_inferences, curr_encodings):
        # TODO check this tolerance value, maybe implement adaptive tolerance for hard cases?
        ret = face_recognition.compare_faces(all_encodings, encoding, tolerance=0.3)
        ret = [1 if x else 0 for x in ret]
        rets[sum(ret)] += 1
        # print(rets)
        # Same faces found in earlier iteration: Append to corresponding data after filling gaps there
        if sum(ret) == 1:
            person_index = ret.index(1)
            diff = t - len(person_data[person_index][0]) - 1
        if sum(ret) == 0:
            all_encodings.append(encoding)
            person_index = len(all_encodings) - 1
            diff = t
            person_data.append([[], [], [], []])
        for i in range(4):
            # Saving like this (4 lists of len t per person) is bad memory access,
            # but better for later evaluation
            person_data[person_index][i].extend([-1] * diff)
            person_data[person_index][i].append(preds[i])

    # Fill up for person data for faces which where not found in this frame.
    # All data will have the same length now.
    person_data = fill_up_inference_data(person_data, t)
    return person_data, all_encodings


# ! Errors:
# ! - Reloading after no faces in lecture (ignore: only relevant while debugging)
def main():
    # read config (developer info)
    root = yaml.safe_load(open("config.yml"))["root"]
    model_path = yaml.safe_load(open("config.yml"))["model"]
    log_dir = yaml.safe_load(open("config.yml"))["logs"]
    interval = int(yaml.safe_load(open("config.yml"))["inference_interval"])

    # load model
    model = get_func_model()
    model.load_weights(model_path)

    # read from gui:
    # gui_start = gui.guiStart.guiStart()
    # lecture_name = gui_start.LectureName
    # input_via = getattr(io_utils.screen_grab, gui_start.InputMethod.lower())
    # performance_mode = gui_start.PerformanceMode
    # session_duration = gui_start.Duration
    lecture_name = "Test2"
    input_via = io_utils.screen_grab.screenshot
    performance_mode = False
    session_duration = 90

    # If the last session was less than session_duration ago, use that sessions data (probably crash/pause)
    time_diff = persistence.last_session_difference(log_dir, lecture_name)
    extend_session = False if time_diff > session_duration else True
    print(time_diff)
    # 2 Lists for Results, because time is more important than memory
    if extend_session:
        # ? Test for edge cases
        save_in = persistence.get_latest_session_path(log_dir, lecture_name)
        all_encodings, person_data = persistence.load_last_session(log_dir, lecture_name, as_lists=True)
        # print(f"loaded array: \n{person_data}")
        vis_data = gui.plots.vis_data()
        vis_data.reload_old_data(person_data)
    else:
        save_in = persistence.get_current_session_path(log_dir, lecture_name)
        person_data = list()
        all_encodings = list()
        vis_data = gui.plots.vis_data()

    print("go gui")
    gui_running = gui.guiRunning.Application()
    print("gui called")

    # TODO get from intra-session ui
    stop = False
    t = 0
    # loop while (not stop button pressed)
    # TODO while not stop:
    # TODO all functions have to work with zero faces too
    for j in range(5):
        iter_start = time.perf_counter()
        imgs = input_via()
        print("image taken")
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
                        longest_t = t
                        t += 1
                        continue
                    # Does not find encodings on just face, needs to take whole image
                    enc = face_recognition.face_encodings(img, [loc])
                    curr_encodings.append(enc[0])
        if not faces:
            longest_t = t
            t += 1
            print("no facesdetected")
            continue
        #gui_running.alpha(vis_data)
        print(f"{len(curr_encodings)} Faces detected")
        # inference
        # Returns array of shape [num_targets=4, num_persons, num_classes=4]
        probs = model.predict(batchify(faces))

        probs = np.array(probs)
        # Reshape to [num_targets=4, num_persons] by taking index of max in last dim
        preds = probs.argmax(axis=2)
        person_preds = preds.T

        # Update visualization data
        vis_data.append_data(preds)

        # In case of pause, fill up for whole sequence. Catch for
        try:
            longest_t = max([len(person[0]) for person in person_data])
            longest_t = max([longest_t, t])
        except:
            longest_t = t

        # match encodings & metrics
        if not performance_mode:
            person_data, all_encodings = manage_encodings(
                person_data, person_preds, all_encodings, curr_encodings, longest_t)

        # TODO update gui with plots
        gui_running.alpha(vis_data)
        #print(vis_data.data)

        t += 1
        print("l T: ", longest_t)
        iter_end = time.perf_counter()
        print(f"Processing one image (with {len(face_locs)} found faces) took {(iter_end-iter_start)} seconds.")
        # Save in certain iterations
        if t % 5 == 0:
            person_data = fill_up_inference_data(person_data, longest_t + 1)
            persistence.save_session(save_in, np.array(all_encodings), np.array(person_data))
        if iter_end - iter_start < interval:
            print("sleep")
            time.sleep(interval - (iter_end - iter_start))
            print("wakey")
        else:
            print("Processing this iteration took longer than inference interval.")
        #gui_running.alpha(vis_data)
    # ? save data (only at end or in fixed intervalls?)
    person_data = fill_up_inference_data(person_data, longest_t + 1)
    print(f"Len Endings save: {len(all_encodings)}")
    print(f"data save: {person_data}")
    print(f"data save shape: {np.array(person_data).shape}")

    persistence.save_session(save_in, np.array(all_encodings), np.array(person_data))


if __name__ == "__main__":
    main()
    # start = time.perf_counter()
    # probs = model.predict(imgs)
    # end = time.perf_counter()
    # print(f"3 images took {end-start} time(s).")
