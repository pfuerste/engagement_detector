import os
import sys
import yaml
# import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('.'))
from models import get_model


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
    model = get_model()
    model.load_weights(os.path.join(model_dir, "checkpoints.hdf5"))
    imgs = [os.path.join(data_root, "DataSet/FaceTest/500044/5000441001/5000441001104.jpg"),
            os.path.join(data_root, "DataSet/FaceTest/500044/5000441001/5000441001121.jpg"),
            os.path.join(data_root, "DataSet/FaceTest/940328/940328016/940328016233.jpg")]
    imgs = [plt.imread(path) for path in imgs]
    imgs = np.array(imgs)
    #print(imgs.shape)
    #print(inference(model, imgs))
    print(model.predict(imgs))
