import os
import yaml
from keras.preprocessing.image import ImageDataGenerator
import pandas as pd


def get_dataframe(subset):
    data_root = yaml.safe_load(open("data/config.yml"))["data_root"]
    label_dir = os.path.join(data_root, "Labels")
    csv_path = os.path.join(label_dir, subset + "ImgLabels.csv")
    df = pd.read_csv(csv_path)
    df["ClipID"] = df["ClipID"].apply(lambda x: x.replace("\\", "/"))
    return df


def get_datagen():
    """Returns keras.preprocessing.image.ImageDataGenerator with image augmentation

    Returns:
        keras.preprocessing.image.ImageDataGenerator
    """
    datagen = ImageDataGenerator(
        rescale=1 / 255.0,
        rotation_range=20,
        zoom_range=0.05,
        width_shift_range=0.05,
        height_shift_range=0.05,
        shear_range=0.05,
        horizontal_flip=True,
        fill_mode="nearest",
        validation_split=0.20)
    return datagen


def get_flowing_datagen(datagen, df, subset, size=None):
    """Returns keras datagen which reads data from pandas dataframe.

    Args:
        datagen (keras.preprocessing.image.ImageDataGenerator)
        df (pandas.DataFrame): Image Dataframe of subset
        subset (str): "Train" or "Validation"

    Returns:
        keras.preprocessing.image.ImageDataGenerator
    """
    root = yaml.safe_load(open("config.yml"))["root"]
    data_root = yaml.safe_load(open(os.path.join(root, "data/config.yml")))["data_root"]
    if os.path.isdir(os.path.join(data_root, "DataSet", "Face" + subset + str(size[0]), "Face" + subset + str(size[0]))):
      subdir = os.path.join(data_root, "DataSet", "Face" + subset + str(size[0]), "Face" + subset + str(size[0]))
    else: 
      subdir = os.path.join(data_root, "DataSet", "Face" + subset + str(size[0]))
    print(f"Subdir: {subdir}")    subset = "training" if subset == "Train" else "validation"
    shuffle = True if subset == "training" else False
    target_size = (32, 32) if not size else size
    datagen = datagen.flow_from_dataframe(
        dataframe=df,
        directory=subdir,
        x_col="ClipID",
        y_col=df.columns.drop("ClipID"),
        subset=subset.lower(),
        batch_size=32,
        seed=42,
        shuffle=shuffle,
        class_mode="raw",
        target_size=target_size)
    return datagen


def reshaped_gen(generator):
    for x, y in generator:
        y = [y[:, 0], y[:, 1], y[:, 2], y[:, 3]]
        yield x, y


if __name__ == "__main__":
    # write_img_csv("Test")
    # write_img_csv("Train")
    # write_img_csv("Validation")

    subset = "Test"
    df = get_dataframe(subset)
    datagen = get_datagen()
    flowing = get_flowing_datagen(datagen, df, subset, (64, 64))
    print(flowing.target_size)

    for data, label in flowing:
        print(label.shape)
        break

    for data, label in reshaped_gen(flowing):
        print(label.shape)
        break
