import os
import sys
import yaml
import tensorflow as tf
import keras
import matplotlib.pyplot as plt
import numpy as np


class PredictionCallback(tf.keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs={}):
        from inference import inference

        data_root = yaml.safe_load(open("config.yml"))["data_root"]
        imgs = [os.path.join(data_root, "DataSet/FaceTest/500044/5000441001/5000441001104.jpg"),
                os.path.join(data_root, "DataSet/FaceTest/500044/5000441001/5000441001121.jpg"),
                os.path.join(data_root, "DataSet/FaceTest/940328/940328016/940328016233.jpg")]
        imgs = [plt.imread(path) for path in imgs]
        imgs = np.array(imgs)
        preds = inference(imgs)
        print('prediction: {} at epoch: {}'.format(preds, epoch))


def train(old_model=None):
    sys.path.insert(0, os.path.abspath('..'))
    sys.path.insert(0, os.path.abspath('.'))
    from models import get_model
    import data.DAiSEE as dai

    print(tf.config.list_physical_devices())

    root = yaml.safe_load(open("config.yml"))["root"]
    model_dir = os.path.join(root, "cnn", "models")
    params = yaml.safe_load(open(os.path.join(root, "cnn/train_config.yml")))
    print("Got Model Params.")

    if old_model:
        model = keras.models.load_model(old_model)
    else:
        model = get_model()

    train_df = dai.get_dataframe("Train")
    val_df = dai.get_dataframe("Validation")
    train_datagen = dai.get_flowing_datagen(dai.get_datagen(), train_df, "Train")
    val_datagen = dai.get_flowing_datagen(dai.get_datagen(), val_df, "Validation")
    print("Got Dataframes.")

    model_checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
        filepath=os.path.join(model_dir, "checkpoints.hdf5"),
        save_weights_only=True,
        monitor='val_mean_squared_error',
        mode='min',
        save_best_only=True)
    callbacks = [model_checkpoint_callback,
                 ]

    print("Got Model, starting to train.")
    model.fit_generator(generator=train_datagen,
                        steps_per_epoch=params["steps"],
                        validation_data=val_datagen,
                        validation_steps=params["val_steps"],
                        epochs=params["epochs"],
                        callbacks=callbacks)
    # model.fit(x=train_datagen,
    #           steps_per_epoch=params["steps"],
    #           validation_data=val_datagen,
    #           validation_steps=params["val_steps"],
    #           epochs=params["epochs"],
    #           callbacks=callbacks)
    #model.save(os.path.join(model_dir, "final_model.h5"))


if __name__ == "__main__":
    # print(tf.config.list_physical_devices())
    # tf.debugging.set_log_device_placement(True)

    # # Create some tensors
    # a = tf.constant([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
    # b = tf.constant([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])
    # c = tf.matmul(a, b)

    # print(c)
    train()
