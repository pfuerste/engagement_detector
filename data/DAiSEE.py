import os
import yaml
from keras.preprocessing.image import ImageDataGenerator
import pandas as pd


def get_dataframe(subset):
    data_root = yaml.safe_load(open("data/config.yml"))["data_root"]
    label_dir = os.path.join(data_root, "Labels")
    csv_path = os.path.join(label_dir, subset + "ImgLabels.csv")
    df = pd.read_csv(csv_path)
    # TODO OS-Abfrage
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


def get_flowing_datagen(datagen, df, subset):
    """Returns keras datagen which reads data from pandas dataframe.

    Args:
        datagen (keras.preprocessing.image.ImageDataGenerator)
        df (pandas.DataFrame): Image Dataframe of subset
        subset (str): "Train" or "Validation"

    Returns:
        keras.preprocessing.image.ImageDataGenerator
    """
    # TODO findet zu wenig Files?
    root = yaml.safe_load(open("config.yml"))["root"]
    data_root = yaml.safe_load(open(os.path.join(root, "data/config.yml")))["data_root"]
    subdir = os.path.join(data_root, "DataSet", "Face" + subset)
    subset = "training" if subset == "Train" else "validation"
    datagen = datagen.flow_from_dataframe(
        dataframe=df,
        directory=subdir,
        x_col="ClipID",
        y_col=list(df.columns.drop("ClipID")),
        subset=subset.lower(),
        batch_size=32,
        seed=42,
        shuffle=True,
        class_mode="raw",
        target_size=(32, 32))
    return datagen


if __name__ == "__main__":
    # write_img_csv("Test")
    # write_img_csv("Train")
    # write_img_csv("Validation")

    subset = "Test"
    df = get_dataframe(subset)
    # print(df.head())
    # print(list(df.columns.drop("ClipID")))
    # print(df.columns)
    datagen = get_datagen()
    flowing = get_flowing_datagen(datagen, df, subset)
    #print(flowing._targets)
    print(flowing.target_size)

    for data, label in flowing:
        print(data)
        print(label)
        # print(len(label))
        # for l in label:
        #     print(l.shape)
        break