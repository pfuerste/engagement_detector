import cv2
import pytest
import matplotlib.pyplot as plt
from input.utils import crop_bbs
from input.face_extract import face_recog_extract


def ugly_imports():
    import os
    import sys
    sys.path.insert(0, os.path.abspath('..'))
    sys.path.insert(0, os.path.abspath('.'))
    from input.utils import crop_bbs
    from input.face_extract import face_recog_extract


# Kein richtiger Test, aber wie soll ich das testen?
def test_it():
    img_path = "input/data/zoom_ui.jpg"
    img = cv2.imread(img_path)
    bbs = face_recog_extract(img_path)
    crops = crop_bbs(img, bbs)
    for crop in crops:
        plt.imshow(crop)
        plt.show()


if __name__ == "__main__":
    pass
