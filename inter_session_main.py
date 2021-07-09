import os
import time
import numpy as np
import sys
import yaml
from io_utils import persistence
from io_utils.utils import crop_bbs
import io_utils.screen_grab
import gui.plots
import gui.guiRunning
import gui.guiStart
from tkinter import *


def main():
    # read config (developer info)
    root = yaml.safe_load(open("config.yml"))["root"]
    model_path = yaml.safe_load(open("config.yml"))["model"]
    log_dir = yaml.safe_load(open("config.yml"))["logs"]
    interval = int(yaml.safe_load(open("config.yml"))["inference_interval"])

    # read from gui:
    # gui_start = gui.guiStart.guiStart()
    # lecture_name = gui_start.LectureName
    # input_via = getattr(io_utils.screen_grab, gui_start.InputMethod.lower())
    # performance_mode = gui_start.PerformanceMode
    # session_duration = gui_start.Duration
    lecture_name = "similar img twic, two lectures"

    # Call the intra-session gui
    root = Tk()
    root.title("Engagement Detector")
    root.geometry("1000x1000+0+0")
    gui_running = gui.guiRunning.Application(master=root)

    sessions_data = gui.plots.Inter_session(log_dir, lecture_name)
    #gui_running.beta(sessions_data)
    gui_running.theta(sessions_data, 0)

    # Start the intra-session gui properly
    gui_running.mainloop()


if __name__ == "__main__":
    main()
    # time.sleep(60)
    # main()
    # time.sleep(60)
    # main()
    # start = time.perf_counter()
    # probs = model.predict(imgs)
    # end = time.perf_counter()
    # print(f"3 images took {end-start} time(s).")
