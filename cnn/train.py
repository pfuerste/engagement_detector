import os
import sys
import yaml


def train():
    sys.path.insert(0, os.path.abspath('..'))
    sys.path.insert(0, os.path.abspath('.'))
    from models import get_model
    import data.DAiSEE as dai

    root = yaml.safe_load(open("config.yml"))["root"]
    data_root = yaml.safe_load(open(os.path.join(root, "data/config.yml")))["data_root"]
    params = yaml.safe_load(open(os.path.join(root, "cnn/train_config.yml")))

    train_df = dai.get_dataframe("Train")
    val_df = dai.get_dataframe("Validation")
    train_datagen = dai.get_flowing_datagen(dai.get_datagen(), train_df, "Train")
    val_datagen = dai.get_flowing_datagen(dai.get_datagen(), val_df, "Validation")

    model = get_model()
    model.fit(x=train_datagen,
              steps_per_epoch=params["steps"],
              validation_data=val_datagen,
              validation_steps=params["val_steps"],
              epochs=params["epochs"])


if __name__ == "__main__":
    train()
