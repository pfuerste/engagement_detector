import os
import yaml
import data.DAiSEE as dai


def test_all_labels_are_files():
    subsets = ["Train", "Test", "Validation"]
    root = yaml.safe_load(open("config.yaml"))["root"]
    data_root = yaml.safe_load(open(os.path.join(root, "data/config.yml")))["data_root"]
    for subset in subsets:
        subdir = os.path.join(data_root, "DataSet", subset)
        df = dai.get_dataframe(subset)
        for _, row in df.iterrows():
            assert os.path.isfile(os.path.join(subdir, row["ClipID"]))
