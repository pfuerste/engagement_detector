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
    from models import get_model, get_func_model
    import data.DAiSEE as dai

    print(tf.config.list_physical_devices())

    # tf.config.threading.set_intra_op_parallelism_threads(10)
    # tf.config.threading.set_inter_op_parallelism_threads(10)

    root = yaml.safe_load(open("config.yml"))["root"]
    model_dir = os.path.join(root, "cnn", "models")
    log_dir = os.path.join(root, "logs")
    params = yaml.safe_load(open(os.path.join(root, "cnn/train_config.yml")))
    print("Got Model Params.")

    if old_model:
        model = keras.models.load_model(old_model)
    else:
        model = get_func_model()

    train_df = dai.get_dataframe("Test")
    val_df = dai.get_dataframe("Validation")
    train_datagen = dai.get_flowing_datagen(dai.get_datagen(), train_df, "Test", (64, 64))
    val_datagen = dai.get_flowing_datagen(dai.get_datagen(), val_df, "Validation", (64, 64))
    train_datagen = dai.reshaped_gen(train_datagen)
    val_datagen = dai.reshaped_gen(val_datagen)
    print("Got Dataframes.")

    model_checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
        filepath=os.path.join(model_dir, "checkpoints.hdf5"),
        save_weights_only=True,
        monitor='val_Engagement_accuracy',
        mode='auto',
        save_best_only=True)
    tb_callback = keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=0,
                                              write_graph=True, write_images=False)
    callbacks = [model_checkpoint_callback,
                 tb_callback]

    # Distribution over all train data computed by data/analysis.py
    bs = [111681, 82821, 41076, 6412]
    es = [1229, 9088, 114112, 117561]
    fs = [157661, 61373, 19867, 3089]
    cs = [187164, 45148, 7907, 1771]
    class_weights = {"Boredom": {0: 1 / bs[0] * sum(bs) / 4, 1: 1 / bs[1] * sum(bs) / 4, 2: 1 / bs[2] * sum(bs) / 4, 3: 1 / bs[3] * sum(bs) / 4},
                     "Engagement": {0: 1 / es[0] * sum(bs) / 4, 1: 1 / es[1] * sum(es) / 4, 2: 1 / es[2] * sum(es) / 4, 3: 1 / es[3] * sum(es) / 4},
                     "Frustration": {0: 1 / fs[0] * sum(fs) / 4, 1: 1 / fs[1] * sum(fs) / 4, 2: 1 / fs[2] * sum(fs) / 4, 3: 1 / fs[3] * sum(fs) / 4},
                     "Confusion": {0: 1 / cs[0] * sum(cs) / 4, 1: 1 / cs[1] * sum(cs) / 4, 2: 1 / cs[2] * sum(cs) / 4, 3: 1 / cs[3] * sum(cs) / 4}
                     }

    print("Got Model, starting to train.")
    model.fit_generator(generator=train_datagen,
                        steps_per_epoch=params["steps"],
                        validation_data=train_datagen,
                        validation_steps=params["val_steps"],
                        epochs=params["epochs"],
                        callbacks=callbacks,
                        class_weight=class_weights,
                        use_multiprocessing=True)
    model.save(os.path.join(model_dir, "final_model.h5"))


if __name__ == "__main__":
    train()
