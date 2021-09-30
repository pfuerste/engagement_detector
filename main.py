import os
import time
import numpy as np
import yaml
import face_recognition
from io_utils import encodings_identity as ei
from io_utils import persistence
from io_utils import face_extract as fe
from io_utils.utils import crop_bbs
import io_utils.screen_grab
from cnn.models import get_func_model, batchify
import gui.plots
import gui.gui_running
import gui.gui_start
import threading
from tkinter import *
import ctypes
import cv2


def fill_up_inference_data(inferences, t, index=None):
    """Extend lists with -1s up to current t

    Args:
        inferences (list): person_data
        t (int): current timestep
        index (int, optional): Only fills person at index if true.
        Defaults to None.

    Returns:
        list: person_data
    """
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


def manage_encodings(
        person_data,
        new_inferences,
        all_encodings,
        curr_encodings,
        t):
    """Managing the encodings

        Args:
            person_data (list): contains person data
            new_inferences : new person prediction
            all_encodings (list): contains known encodings
            curr_encodings (list): containt encodings from current list
            t (int): current timestamp

        """

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
            person_data.append(
                [[-1] * diff, [-1] * diff, [-1] * diff, [-1] * diff])
            person_data[i][0].append(new_inferences[i][0])
            person_data[i][1].append(new_inferences[i][1])
            person_data[i][2].append(new_inferences[i][2])
            person_data[i][3].append(new_inferences[i][3])
        all_encodings = curr_encodings
        return person_data, all_encodings

    # "Usual" case: Found faces during lecture
    rets = dict(zip(range(len(all_encodings) + 1),
                    [0] * (len(all_encodings) + 1)))
    for preds, encoding in zip(new_inferences, curr_encodings):
        ret = face_recognition.compare_faces(
            all_encodings, encoding, tolerance=0.6)
        ret = [1 if x else 0 for x in ret]
        rets[sum(ret)] += 1
        # print(rets)
        # Same faces found in earlier iteration: Append to corresponding data
        # after filling gaps there
        if sum(ret) == 1:
            person_index = ret.index(1)
            diff = t - len(person_data[person_index][0]) - 1
            similarity_handled = True
        # This is a new face, append new list for that person
        if sum(ret) == 0:
            all_encodings.append(encoding)
            person_index = len(all_encodings) - 1
            diff = t
            person_data.append([[], [], [], []])
            similarity_handled = True
        # This person is similar to multiple people from earlier.
        # Decrease Encoding distance iterativly.
        # If still similar to multiples, just ignore the person for this
        # iteration and dont append its data.
        else:
            tol = 0.45
            similarity_handled = False
            for i in range(3):
                tol *= 0.75
                ret = face_recognition.compare_faces(
                    all_encodings, encoding, tolerance=tol)
                ret = [1 if x else 0 for x in ret]
                if sum(ret) == 1:
                    person_index = ret.index(1)
                    diff = t - len(person_data[person_index][0]) - 1
                    similarity_handled = True
                    continue
                if sum(ret) == 0:
                    all_encodings.append(encoding)
                    person_index = len(all_encodings) - 1
                    diff = t
                    person_data.append([[], [], [], []])
                    similarity_handled = True
                    continue

        # Save data for person. Skip if person is duplicate (similar to
        # multiples).
        if similarity_handled:
            for i in range(4):
                # Saving like this (4 lists of len t per person)
                # is bad memory access,
                # but better for later evaluation
                person_data[person_index][i].extend([-1] * diff)
                person_data[person_index][i].append(preds[i])

    # Fill up for person data for faces which where not found in this frame.
    # All data will have the same length now.
    person_data = fill_up_inference_data(person_data, t)
    return person_data, all_encodings


def main():
    def run(vis_data, person_data, all_encodings, gui_running, window=None):
        """mainloop with taking picture, find/extract/encode faces,
        put them into the model, show data until end variable is set

        Args:
            vis_data: class plots.vis_data
            person_data (list): contains person data
            all_encodings (list): contains known encodings
            gui_running: class gui_running
            window (string): window name from the captured window

        """
        # Make windowgrab DPI-aware incase of Resolution scaling
        awareness = ctypes.c_int()
        ctypes.windll.shcore.SetProcessDpiAwareness(2)

        t = 0
        model = get_func_model()
        model.load_weights(model_path)
        model._make_predict_function()
        # for i in range(5):
        while not gui_running.get_end():
            iter_start = time.perf_counter()
            if window:
                if io_utils.screen_grab.window_out_of_screen(window):
                    gui_running.window_warning(
                        "Please maximize the lecture input window in the background.")
                time.sleep(5)
                imgs = input_via(window)
            else:
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
                    if not performance_mode:
                        if not faces:
                            longest_t = t
                            t += 1
                            continue
                        # Does not find encodings on just face, needs to take
                        # whole image
                        enc = face_recognition.face_encodings(img, [loc])
                        curr_encodings.append(enc[0])
            if not faces:
                longest_t = t
                t += 1
                print("no faces detected")
                continue

            probs = model.predict(batchify(faces))
            probs = np.array(probs)
            # Reshape to [num_targets=4, num_persons] by taking index of max in
            # last dim
            preds = probs.argmax(axis=2)
            person_preds = preds.T

            # Update visualization data
            vis_data.append_data(preds)

            # In case of pause, fill up for whole sequence. Catch for
            try:
                longest_t = max([len(person[0]) for person in person_data])
                longest_t = max([longest_t, t])
            except BaseException:
                longest_t = t

            # match encodings & metrics
            if not performance_mode:
                person_data, all_encodings = manage_encodings(
                    person_data, person_preds, all_encodings, curr_encodings, longest_t)
            try:
                gui_running.intra_avg_plot(vis_data)
            # GUI already closed
            except RuntimeError:
                pass

            t += 1
            iter_end = time.perf_counter()
            # print(f"Processing one image (with {len(face_locs)} found faces)
            # took {(iter_end-iter_start)} seconds.")
            # Save in certain iterations
            if t % 5 == 0:
                person_data = fill_up_inference_data(
                    person_data, longest_t + 1)
                persistence.save_session(
                    save_in, np.array(all_encodings), np.array(person_data))
            if iter_end - iter_start < interval:
                time.sleep(interval - (iter_end - iter_start))
            else:
                print("Processing this iteration took longer than inference interval.")
        person_data = fill_up_inference_data(person_data, longest_t + 1)
        persistence.save_session(
            save_in,
            np.array(all_encodings),
            np.array(person_data))
        time.sleep(5)
        os._exit(1)

    # read config (developer info)
    root = yaml.safe_load(open("config.yml"))["root"]
    model_path = yaml.safe_load(open("config.yml"))["model"]
    log_dir = yaml.safe_load(open("config.yml"))["logs"]
    interval = int(yaml.safe_load(open("config.yml"))["inference_interval"])
    keep_top = bool(yaml.safe_load(open("config.yml"))["keep_top"])

    # load model
    model = get_func_model()
    model.load_weights(model_path)
    model._make_predict_function()

    # read from gui:
    gui_start = gui.gui_start.gui_start(
        persistence.get_old_lecture_names(log_dir))
    lecture_name = gui_start.lecture_name
    input_via = getattr(io_utils.screen_grab, gui_start.input_method.lower())
    if gui_start.input_method.lower() == "window_grab":
        window = gui_start.window_name
    else:
        window = None
    performance_mode = gui_start.performance_mode
    session_duration = gui_start.duration

    # If the last session was less than session_duration ago, use that
    # sessions data (probably crash/pause)
    time_diff = persistence.last_session_difference(log_dir, lecture_name)
    extend_session = False if time_diff > session_duration else True
    # 2 Lists for Results, because time is more important than memory
    if extend_session:
        save_in = persistence.get_latest_session_path(log_dir, lecture_name)
        try:
            all_encodings, person_data = persistence.load_last_session(
                log_dir, lecture_name, as_lists=True)
            vis_data = gui.plots.Vis_data()
            vis_data.reload_old_data(person_data)
        except FileNotFoundError:
            person_data = list()
            all_encodings = list()
            vis_data = gui.plots.Vis_data()
    else:
        save_in = persistence.get_current_session_path(log_dir, lecture_name)
        person_data = list()
        all_encodings = list()
        vis_data = gui.plots.Vis_data()

    # Call the intra-session gui
    root = Tk()
    root.title("Engagement Detector")
    root.geometry("600x400+0+0")
    if keep_top:
        root.wm_attributes("-topmost", 1)
    gui_running = gui.gui_running.Application(master=root)

    # Save incase of early crash/pause
    persistence.save_session(
        save_in,
        np.array(all_encodings),
        np.array(person_data))
    # Start the thread for getting data so GUI doesn't freeze
    t1 = threading.Thread(
        target=run,
        args=(
            vis_data,
            person_data,
            all_encodings,
            gui_running,
            window))
    t1.start()

    # Start the intra-session gui properly
    gui_running.mainloop()


if __name__ == "__main__":
    main()
