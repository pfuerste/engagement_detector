import os
import sys
from face_recognition.api import face_encodings
import yaml
import tqdm
import numpy as np
import matplotlib.pyplot as plt
import face_recognition as fr
from sklearn.metrics import confusion_matrix, accuracy_score, mean_squared_error
sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('.'))
from models import get_model, get_func_model
import data.DAiSEE as dai
from io_utils import face_extract as fe
from io_utils.utils import crop_bbs


def test_model(model, generator, num=1):
    # Create lists for storing the predictions and labels
    b_predictions = []
    b_labels = []
    e_predictions = []
    e_labels = []
    f_predictions = []
    f_labels = []
    c_predictions = []
    c_labels = []

    # Loop over the generator
    for data, label in generator:
        b_labels.extend([l[0] for l in label])
        e_labels.extend([l[1] for l in label])
        c_labels.extend([l[2] for l in label])
        f_labels.extend([l[3] for l in label])

        # b_labels.extend(np.argmax(label[0], axis=1))
        # e_labels.extend(np.argmax(label[1], axis=1))
        # c_labels.extend(np.argmax(label[2], axis=1))
        # f_labels.extend(np.argmax(label[3], axis=1))

        # Make predictions on data using the model. Store the results.
        preds = model.predict(data)
        b_predictions.extend(np.argmax(preds[0], axis=1))
        e_predictions.extend(np.argmax(preds[1], axis=1))
        c_predictions.extend(np.argmax(preds[2], axis=1))
        f_predictions.extend(np.argmax(preds[3], axis=1))

        # We have to break out from the generator when we've processed
        # the entire once (otherwise we would end up with duplicates).
        if len(b_predictions) == num * 32:
            break

    # print(list(zip(b_labels, b_predictions)))
    # print(list(zip(e_labels, e_predictions)))
    # print(len(b_labels), len(b_predictions))
    b_acc = accuracy_score(b_labels, b_predictions)
    b_mse = mean_squared_error(b_labels, b_predictions)
    print(f"b_acc: {b_acc}")
    print(f"b_mse: {b_mse}")
    b_matrix = confusion_matrix(b_labels, b_predictions, labels=[0, 1, 2, 3])
    # print(b_matrix)

    e_acc = accuracy_score(e_labels, e_predictions)
    e_mse = mean_squared_error(e_labels, e_predictions)
    print(f"e_acc: {e_acc}")
    print(f"e_mse: {e_mse}")
    e_matrix = confusion_matrix(e_labels, e_predictions, labels=[0, 1, 2, 3])
    # print(e_matrix)

    f_acc = accuracy_score(f_labels, f_predictions)
    f_mse = mean_squared_error(f_labels, f_predictions)
    print(f"f_acc: {f_acc}")
    print(f"f_mse: {f_mse}")
    f_matrix = confusion_matrix(f_labels, f_predictions, labels=[0, 1, 2, 3])
    # print(f_matrix)

    c_acc = accuracy_score(c_labels, c_predictions)
    c_mse = mean_squared_error(c_labels, c_predictions)
    print(f"c_acc: {c_acc}")
    print(f"c_mse: {c_mse}")
    c_matrix = confusion_matrix(c_labels, c_predictions, labels=[0, 1, 2, 3])
    # print(c_matrix)


def test_face_recog(data_root):
    def get_big_dirs(test_root, frames):
        min_len = 0
        while min_len < frames:
            subject_dirs = [
                os.path.join(
                    test_root,
                    x) for x in np.random.choice(
                    os.listdir(test_root),
                    m,
                    replace=False)]
            test_dirs = [os.path.join(s_dir, np.random.choice(os.listdir(s_dir), replace=False))
                         for s_dir in subject_dirs]
            min_len = min([len(os.listdir(test_dir)) for test_dir in test_dirs])
        return test_dirs

    m = 16
    n = 16
    frames = 20
    # get random dirs of follow-up frames
    test_root = os.path.join(data_root, "DataSet", "FaceTest64")
    # Some dirs are to small to retrieve enough frames
    test_dirs = get_big_dirs(test_root, frames)
    imgs = {test_dir: list() for test_dir in test_dirs}

    # retrieve similar frames for all subjects
    for test_dir in test_dirs:
        i = os.listdir(test_dir)[:frames]
        for frame in i:
            imgs[test_dir].append(plt.imread(os.path.join(test_dir, frame)))
            dtype = imgs[test_dir][-1].dtype

    # dicts are not ordered but we want easy indexed access
    ind_to_dict = dict()
    dict_to_int = dict()
    for i, d in enumerate(test_dirs):
        ind_to_dict[i] = d
        dict_to_int[d] = i

    # generate gts: list with dict of indices per frame
    gts = list()
    # generate empty images and fill them with random persons' frames
    bar_size = 10
    dummy_vid = np.zeros((64 * 2 + 3 * bar_size, 64 * 8 + 9 * bar_size, frames * 3), dtype=dtype)
    for f in range(frames):
        rand_inds = np.random.choice(range(len(test_dirs)), n, replace=False)
        gts.append({ind: ind_to_dict[ind] for ind in rand_inds})
        for i in range(int(n / (n / 2))):
            for j in range(int(n / 2)):
                paste = imgs[ind_to_dict[rand_inds[i * int(n / 2) + j]]][f]
                dummy_vid[(i + 1) * bar_size + i * 64:(i + 1) * bar_size +
                          i * 64 + 64, (j + 1) * bar_size + j * 64:(j + 1) * bar_size + j * 64 + 64, f * 3:f * 3 + 3] = paste

    # run face detection and save number of detected faces for each frame
    num_detections = list()
    encodings = list()
    for i in range(frames):
        img = dummy_vid[..., i * 3:i * 3 + 3]
        locs = fe.face_recog_extract(img)
        detections = []
        for loc in locs:
            detections.append(loc)
        num_detections.append(len(detections))
        encodings.append(fr.face_encodings(img, detections))

    # check if there is always exactly one similar face in the next frame (as it should be)
    all_hits = list()
    for f in range(frames - 1):
        for enc in encodings[f]:
            tol = 0.6
            ret = fr.compare_faces(encodings[f + 1], enc, tolerance=tol)
            ret = [1 if x else 0 for x in ret]
            hits = sum(ret)
            if hits > 1:
                for i in range(3):
                    tol *= 0.75
                    ret = fr.compare_faces(encodings[f + 1], enc, tolerance=tol)
                    ret = [1 if x else 0 for x in ret]
                    hits = sum(ret)
                    if hits <= 1:
                        all_hits.append(hits)
                        continue
                    elif i == 2:
                        all_hits.append(hits)
                    else:
                        pass

    return(len(all_hits), sum(all_hits), num_detections)


if __name__ == "__main__":
    root = yaml.safe_load(open("config.yml"))["root"]
    data_root = yaml.safe_load(open("config.yml"))["data_root"]
    model_dir = os.path.join(root, "cnn", "models")

    def start_model_test():
        model = get_func_model()
        model.load_weights(os.path.join(model_dir, "untuned_final_func.hdf5"))
        test_df = dai.get_dataframe("Test")
        test_datagen = dai.get_flowing_datagen(dai.get_datagen(), test_df, "Test", (64, 64))

        test_model(model, test_datagen, 500)

    global_acc_compares, global_acc_detections = 0, 0
    num = 50
    for i in tqdm.tqdm(range(num)):
        num_tests, num_right, num_detections = test_face_recog(data_root)
        acc_compares = num_right/num_tests
        print(acc_compares)
        acc_detections = sum([frame/16 for frame in num_detections])/20
        print(acc_detections)
        global_acc_compares += acc_compares
        global_acc_detections += acc_detections
    print(f"Accuracy for detections of faces after {num} trials of mock-up videos: {global_acc_detections/num}")
    print(f"Accuracy for compares of faces (regarding number of recognized faces in each next frame) after {num} trials of mock-up videos: {global_acc_compares/num}")
