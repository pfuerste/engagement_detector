import os
import yaml
from keras.preprocessing.image import ImageDataGenerator
import pandas as pd


def write_img_csv(subset):
    """Write image labels to csv from video labels.

    Args:
        subset (str): "Train", "Test", or "Validation"

    Raises:
        FileExistsError: if image label csv already exists
    """    
    data_root = yaml.safe_load(open("data/config.yml"))["data_root"]
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


def get_datagen():
    """Returns keras.preprocessing.image.ImageDataGenerator with image augmentation

    Returns:
        keras.preprocessing.image.ImageDataGenerator
    """
    # Image augmentation params
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
        subset (str): "Training" or "Validation"

    Returns:
        keras.preprocessing.image.ImageDataGenerator
    """
    data_root = yaml.safe_load(open("data/config.yml"))["data_root"]
    subdir = os.path.join(data_root, "DataSet", subset)
    print(subdir)
    subset = "training" if subset == "Train" else "validation"
    datagen = datagen.flow_from_dataframe(
        dataframe=df,
        directory=subdir,
        x_col="ClipID",
        y_col=["Boredom", "Engagement", "Confusion", "Frustration "],
        subset=subset.lower(),
        batch_size=32,
        seed=42,
        shuffle=True,
        class_mode="raw",
        target_size=(32, 32))
    return datagen


if __name__ == "__main__":
    write_img_csv("Test")
    # subset = "Train"
    # df = get_dataframe(subset)
    # print(df.head())
    # print(df.columns)
    # datagen = get_datagen()
    # flowing = get_flowing_datagen(datagen, df, subset)
