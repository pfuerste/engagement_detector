import os
import sys
import yaml
# import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('.'))
from models import get_model, get_func_model
import time


def inference(model, img_list):
    preds = list()
    for img in img_list:
        pred = model.predict(img)
        preds.append(pred)
    return preds


if __name__ == "__main__":
    root = yaml.safe_load(open("config.yml"))["root"]
    data_root = yaml.safe_load(open("config.yml"))["data_root"]
    model_dir = os.path.join(root, "cnn", "models")
    model = get_func_model()
    model.load_weights(os.path.join(model_dir, "checkpoints_func.hdf5"))
    imgs = [os.path.join(data_root, "DataSet/FaceTest32/500044/5000441001/5000441001104.jpg")]
            # os.path.join(data_root, "DataSet/FaceTest32/500044/5000441001/5000441001121.jpg"),
            # os.path.join(data_root, "DataSet/FaceTest32/940328/940328016/940328016233.jpg")]
    imgs = [plt.imread(path) for path in imgs]
    imgs = np.array(imgs)
    #print(imgs.shape)
    #print(inference(model, imgs))
    start = time.perf_counter()
    preds = model.predict(imgs)
    end = time.perf_counter()
    print(f"3 images took {end-start} time(s).")

    print(len(preds))
    for pred in preds:
        print(pred, "\n")
