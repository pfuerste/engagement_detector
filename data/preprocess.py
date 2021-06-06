import os
import sys
import yaml
import pandas as pd
import cv2 as cv
import tqdm
import multiprocessing
from joblib import Parallel, delayed
import time
import random


def write_img_csv(subset):
    """Write image labels to csv from video label csv.

    Args:
        subset (str): "Train", "Test", or "Validation"

    Raises:
        FileExistsError: if image label csv already exists
    """
    root = yaml.safe_load(open("config.yml"))["root"]
    data_root = yaml.safe_load(open(os.path.join(root, "data/config.yml")))["data_root"]
    subdir = os.path.join(data_root, "DataSet", subset)

    avi_csv_path = os.path.join(data_root, "Labels", subset + "Labels.csv")
    img_csv_path = os.path.join(data_root, "Labels", subset + "ImgLabels.csv")
    if os.path.isfile(img_csv_path):
        raise FileExistsError(
            f"""Labels for image files are already processed
            please check and delete if wanted. File Location: {img_csv_path}""")
    avi_df = pd.read_csv(avi_csv_path)
    with open(img_csv_path, "w") as csv:
        csv.write("ClipID, Boredom, Engagement, Confusion, Frustration \n")
        for _, row in avi_df.iterrows():
            clip_id = row["ClipID"].replace(".avi", "").replace(".mp4", "")
            subj_dir = clip_id[:6]
            label_str = str(row["Boredom"]) + ", " + str(row["Engagement"]) + ", " + \
                str(row["Confusion"]) + ", " + str(row["Frustration "])
            img_files = [file for file in os.listdir(os.path.join(subdir, subj_dir, clip_id)) if file.endswith(".jpg")]

            for img_file in img_files:
                csv.write(os.path.join(subj_dir, clip_id, img_file) + ", " + label_str + " \n")


def create_face_data(subset):
    sys.path.insert(0, os.path.abspath('..'))
    sys.path.insert(0, os.path.abspath('.'))
    import input.face_extract as fe
    import input.utils as utils

    root = yaml.safe_load(open("config.yml"))["root"]
    data_root = yaml.safe_load(open(os.path.join(root, "data/config.yml")))["data_root"]
    subdir = os.path.join(data_root, "DataSet", subset)
    user_dirs = [os.path.join(subdir, dir) for dir in os.listdir(subdir)
                 if os.path.isdir(os.path.join(subdir, dir))]
    img_paths = list()
    for user_dir in user_dirs:
        vid_dirs = [os.path.join(user_dir, dir) for dir in os.listdir(user_dir)
                    if os.path.isdir(os.path.join(user_dir, dir))]
        for vid_dir in vid_dirs:
            img_files = [os.path.join(vid_dir, file) for file in os.listdir(vid_dir) if file.endswith(".jpg")]
            img_paths.extend(img_files)

    def extract_and_copy(img_path):
        # for old_path in tqdm.tqdm(img_paths):
        split = img_path.split(os.sep + subset + os.sep)
        split2 = split[1].split(os.sep)
        split3 = split2[0] + os.sep + split2[1]
        if not os.path.isdir(os.path.join(split[0], "Face" + subset, split3)):
            os.makedirs(os.path.join(split[0], "Face" + subset, split3))
            # os.mkdir(os.path.join(split[0], "Face" + subset))

        new_path = os.path.join(split[0], "Face" + subset, split[1])
        if os.path.isfile(new_path):
            return 0
            # continue
        img = cv.imread(img_path)
        bb = fe.face_recog_extract(img)
        face_img = utils.crop_bbs(img, bb)
        # Ignore ambigous images, keras generator should skip them too
        if len(face_img) != 1:
            return 0
            # continue
        # Only one face per image in train set
        face_img = cv.resize(face_img[0], (32, 32))
        cv.imwrite(new_path, face_img)

    start = time.perf_counter()
    random.shuffle(img_paths)
    img_paths = tqdm.tqdm(img_paths)
    #Parallel(n_jobs=-1)(delayed(extract_and_copy)(i) for i in img_paths)
    for i in img_paths:
        extract_and_copy(i)
    end = time.perf_counter()
    print(f"preocessing faces took {end-start} time(s).")


if __name__ == "__main__":
    create_face_data("dev")
