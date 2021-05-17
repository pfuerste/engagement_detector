import yaml
import os
from PIL import ImageGrab
from datetime import datetime
from time import sleep


def take_screenshot():
    im = ImageGrab.grab()
    dt = datetime.now()
    fname = os.path.join("input", "data", "pic_{}.{}.png".format(
        dt.strftime("%H%M_%S"), dt.microsecond // 100000))
    im.save(fname, 'png')


if __name__ == "__main__":
    conf = yaml.safe_load(open("input/config.yml"))
    while True:
        take_screenshot()
        sleep(conf["sleep_seconds"])
