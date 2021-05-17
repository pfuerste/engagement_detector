import yaml
import os
from PIL import ImageGrab
from datetime import datetime
from time import sleep

conf = yaml.safe_load(open("input/config.yml"))
while True:
    im = ImageGrab.grab()
    dt = datetime.now()
    fname = os.path.join("input", "data", "pic_{}.{}.png".format(
        dt.strftime("%H%M_%S"), dt.microsecond // 100000))
    im.save(fname, 'png')
    sleep(conf["sleep_seconds"])
