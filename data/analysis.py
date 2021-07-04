import os
import sys
import yaml
import numpy as np
sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('.'))
import data.DAiSEE as dai


if __name__ == "__main__":

    bs = [111681,  82821,  41076,   6412]
    es = [1229,   9088, 114112, 117561]
    fs = [157661,  61373,  19867,   3089]
    cs = [187164,  45148,   7907,   1771]
    class_weights = {"Boredom": {"0":1 / bs[0] * sum(bs) / 4, "1":1 / bs[1] * sum(bs) / 4, "2":1 / bs[2] * sum(bs) / 4, "3":1 / bs[3] * sum(bs) / 4},
                     "Engagement": {"0": 1 / es[0] * sum(bs) / 4, "1": 1 / es[1] * sum(es) / 4, "2": 1 / es[2] * sum(es) / 4, "3": 1 / es[3] * sum(es) / 4},
                     "Frustration": {"0": 1 / fs[0] * sum(fs) / 4, "1": 1 / fs[1] * sum(fs) / 4, "2": 1 / fs[2] * sum(fs) / 4, "3": 1 / fs[3] * sum(fs) / 4},
                     "Confusion": {"0": 1 / cs[0] * sum(cs) / 4, "1": 1 / cs[1] * sum(cs) / 4, "2": 1 / cs[2] * sum(cs) / 4, "3": 1 / cs[3] * sum(cs) / 4}
                     }

    print(class_weights)
    # root = yaml.safe_load(open("config.yml"))["root"]
    # data_root = yaml.safe_load(open("config.yml"))["data_root"]
    # model_dir = os.path.join(root, "cnn", "models")

    # test_df = dai.get_dataframe("Train")
    # test_datagen = dai.get_flowing_datagen(dai.get_datagen(), test_df, "Train", (32, 32))

    # b, e, f, c = np.zeros((4)), np.zeros((4)), np.zeros((4)), np.zeros((4))
    # for label in test_datagen.labels:
    #     b[label[0]] += 1
    #     e[label[1]] += 1
    #     c[label[2]] += 1
    #     f[label[3]] += 1
    # print(b)
    # print(e)
    # print(c)
    # print(f)

    # TODO dhould be a test
    # Check validity of reshape-generator:
    # test_datagen = dai.reshaped_gen(test_datagen, 1)
    # all = np.zeros((4, 4))
    # for ind, (data, label) in enumerate(test_datagen):
    #     for i, list in enumerate(label):
    #         for j in list:
    #             all[i, j] += 1
    #     if ind > 17000 / 32:
    #         break
    # print(all)
