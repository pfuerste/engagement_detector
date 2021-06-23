import os
import sys
import yaml
import numpy as np
sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('.'))
import data.DAiSEE as dai


if __name__ == "__main__":
    root = yaml.safe_load(open("config.yml"))["root"]
    data_root = yaml.safe_load(open("config.yml"))["data_root"]
    model_dir = os.path.join(root, "cnn", "models")

    test_df = dai.get_dataframe("Test")
    test_datagen = dai.get_flowing_datagen(dai.get_datagen(), test_df, "Test")

    b, e, f, c = np.zeros((4)), np.zeros((4)), np.zeros((4)), np.zeros((4))
    for label in test_datagen.labels:
        b[label[0]] += 1
        e[label[1]] += 1
        c[label[2]] += 1
        f[label[3]] += 1
    print(b)
    print(e)
    print(c)
    print(f)

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
