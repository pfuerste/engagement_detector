import os
import time
import numpy as np
import sys
import yaml
from io_utils import persistence
from io_utils.utils import crop_bbs
import io_utils.screen_grab
import gui.plots
import gui.gui_running
import gui.inter_session_gui_start
from tkinter import *


def main():
    # read config (developer info)
    root = yaml.safe_load(open("config.yml"))["root"]
    log_dir = yaml.safe_load(open("config.yml"))["logs"]

    # read from gui:
    gui_start = gui.inter_session_gui_start.Inter_session_gui_start(persistence.get_old_lecture_names(log_dir))

    # Call the intra-session gui
    root = Tk()
    root.title("Engagement Detector")
    root.geometry("1000x800+0+0")
    gui_running = gui.gui_running.Application(master=root)

    sessions_data = gui.plots.Inter_session(log_dir, gui_start.lecture_name)
    print(log_dir)
    if gui_start.average_data is True:
        gui_running.inter_avg_plot(sessions_data)
    elif gui_start.single_data is True:
        gui_running.inter_emo_plot(sessions_data, gui_start.emotion)

    # Start the intra-session gui properly
    gui_running.mainloop()


if __name__ == "__main__":
    main()
