import os
import sys
import yaml
import tqdm
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import confusion_matrix, accuracy_score, mean_squared_error
sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('.'))
from models import get_model, get_func_model
import data.DAiSEE as dai


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
        b_labels.extend(label[0])
        e_labels.extend(label[1])
        c_labels.extend(label[2])
        f_labels.extend(label[3])

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

    print(list(zip(b_labels, b_predictions)))
    print(list(zip(e_labels, e_predictions)))

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


if __name__ == "__main__":
    root = yaml.safe_load(open("config.yml"))["root"]
    data_root = yaml.safe_load(open("config.yml"))["data_root"]
    model_dir = os.path.join(root, "cnn", "models")
    model = get_func_model()
    model.load_weights(os.path.join(model_dir, "untuned_final_func.hdf5"))

    test_df = dai.get_dataframe("Test")
    test_datagen = dai.get_flowing_datagen(dai.get_datagen(), test_df, "Test", (64, 64))

    test_model(model, test_datagen, 17000/32)
