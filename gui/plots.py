import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)
from tkinter import *
import tkinter as tk
import sys
import os
sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('.'))
from io_utils.persistence import get_sorted_session_paths, load_last_session, load_all_sessions


class Vis_data():
    """Saves data for visualization to not do calculations more often
    than needed for live plotting.
    """

    def __init__(self):
        self.data = [[], [], [], []]
        self.avg_boredom = []
        self.avg_engagement = []
        self.avg_confusion = []
        self.avg_frustration = []

    def reload_old_data(self, person_data):
        scores = np.array(person_data)
        if scores.size == 0:
            # Else reloading on empty data crashes
            return
        data = np.swapaxes(scores, 0, 1)
        data = np.swapaxes(data, 1, 2)
        data = [[[p for p in emotion] for emotion in t] for t in data]
        self.data = data
        self.avg_boredom = []
        self.avg_engagement = []
        self.avg_confusion = []
        self.avg_frustration = []
        for t in range(len(data[0])):
            try:
                self.avg_boredom.append(sum([x for x in data[0][t] if x != -1]) /
                                        len([x for x in data[0][t] if x != -1]))
            except ZeroDivisionError:
                self.avg_boredom.append(-1)
            try:
                self.avg_engagement.append(sum([x for x in data[1][t] if x != -1]) /
                                           len([x for x in data[1][t] if x != -1]))
            except ZeroDivisionError:
                self.avg_engagement.append(-1)
            try:
                self.avg_confusion.append(sum([x for x in data[2][t] if x != -1]) /
                                          len([x for x in data[2][t] if x != -1]))
            except ZeroDivisionError:
                self.avg_confusion.append(-1)
            try:
                self.avg_frustration.append(sum([x for x in data[3][t] if x != -1]) /
                                            len([x for x in data[3][t] if x != -1]))
            except ZeroDivisionError:
                self.avg_frustration.append(-1)

    def append_data(self, new_data):
        for i, emo_data in enumerate(new_data):
            self.data[i].append(emo_data)
        self.append_averages(new_data)

    def append_averages(self, new_data):
        new_averages = [sum(x) / len(x) for x in new_data]
        self.avg_boredom.append(new_averages[0])
        self.avg_engagement.append(new_averages[1])
        self.avg_confusion.append(new_averages[2])
        self.avg_frustration.append(new_averages[3])

    def current_avgs(self):
        return self.avg_boredom[-1], self.avg_engagement[-1], \
            self.avg_confusion[-1], self.avg_frustration[-1]

    def current_data(self):
        return [self.data[0][-1], self.data[1][-1], self.data[2][-1], self.data[3][-1]]

    def is_critical_level(self, share=0.1):
        curr = self.current_data()
        people = len(curr[0])
        critical = []
        for i, emo in enumerate(curr):
            if i == 1:
                critical.append(sum([1 if x == 0 else 0 for x in emo]))
            else:
                critical.append(sum([1 if x == 3 else 0 for x in emo]))
        critical = [True if x > people * share else False for x in critical]
        return critical

    # intra-session plotting
    def get_avg_plots(self, window):
        if window.widget:
            window.widget.destroy()
        # break if used without data
        if not self.avg_boredom:
            fig, (ax0, ax1) = plt.subplots(2, 1)
        else:
            fig, (ax0, ax1) = plt.subplots(2, 1)
            ax0.set_ylim(-1, 4)
            ax0.bar(x=["Boredom", "Engagement", "Confusion", "Frustration"],
                    height=self.current_avgs(),
                    color=["black", "green", "purple", "red"],
                    label=["black", "green", "purple", "red"])
            critical = self.is_critical_level()
            for i, v in enumerate(critical):
                if v:
                    ax0.text(x=i - 0.1, y=1, s="!", color='y', fontweight='bold', fontsize=30)

            ax1.set_ylim(-1, 4)
            ax1.grid()
            ax1.plot(range(1, len(self.avg_boredom) + 1), self.avg_boredom, c="black")
            ax1.plot(range(1, len(self.avg_boredom) + 1), self.avg_engagement, c="green")
            ax1.plot(range(1, len(self.avg_boredom) + 1), self.avg_confusion, c="purple")
            ax1.plot(range(1, len(self.avg_boredom) + 1), self.avg_frustration, c="red")

            canvas = FigureCanvasTkAgg(fig, master=window.master)
            window.widget = canvas.get_tk_widget()
            window.widget.pack(fill=BOTH)
            


# inter-session plotting
class Inter_session():

    def __init__(self, log_dir, lecture_name):
        self.sessions_data = load_all_sessions(log_dir, lecture_name, True)
        self.session_lengths = []

    def get_avg_plots(self, window):
        #TODO broken axis for -1s? 
        self.sessions_vis_data = []
        self.avg_boredom = []
        self.avg_engagement = []
        self.avg_confusion = []
        self.avg_frustration = []
        for scores in self.sessions_data[1]:
            _vis_data = Vis_data()
            _vis_data.reload_old_data(scores)
            self.sessions_vis_data.append(_vis_data)
            self.session_lengths.append(len(_vis_data.data[0]))
        for vis_data in self.sessions_vis_data:
            print(vis_data.avg_boredom)
            self.avg_boredom.extend(vis_data.avg_boredom)
            self.avg_engagement.extend(vis_data.avg_engagement)
            self.avg_confusion.extend(vis_data.avg_confusion)
            self.avg_frustration.extend(vis_data.avg_frustration)
        #if window.widget:
        #    window.widget.destroy()

        # break if used without data
        if not self.avg_boredom:
            fig, ax1 = plt.subplots(1, 1)
        else:
            fig, ax1 = plt.subplots(1, 1)
            ax1.set_ylim(-1, 4)
            ax1.grid()
            ax1.plot(range(1, len(self.avg_boredom) + 1), self.avg_boredom, c="black")
            ax1.plot(range(1, len(self.avg_boredom) + 1), self.avg_engagement, c="green")
            ax1.plot(range(1, len(self.avg_boredom) + 1), self.avg_confusion, c="purple")
            ax1.plot(range(1, len(self.avg_boredom) + 1), self.avg_frustration, c="red")
            sess_end = 0
            for i, time_stamp in enumerate(self.session_lengths):
                if i == len(self.session_lengths) - 1:
                    continue
                sess_end += time_stamp
                ax1.axvline(x=sess_end, linestyle="dashed")
        canvas = FigureCanvasTkAgg(fig, master=window.master)
        window.toolbar = NavigationToolbar2Tk(canvas,window)
        window.toolbar.update()
        window.widget = canvas.get_tk_widget()
        window.widget.pack(fill=BOTH)
        window.toolbars = canvas._tkcanvas
        window.toolbars.pack(fill=BOTH)

    def get_emotion_plot(self, window, emo_ind):
        self.person_data = []

        for id in self.sessions_data[0]:
            print(np.array(id).shape)
        for session in self.sessions_data[1]:
            print(np.array(session).shape)
            self.session_lengths.append(np.array(session).shape[-1])
        # TODO Create BIG array of semester length with -1s whernever someone wasnt there
        # know how many people: counter = 0, first session: add num_ids; for other session: for encoding, check if already in, else counter++ 
        # Create array -1s of shape (num_people, all_timesteps)
        # for session: put person @ its slot
        fig, ax0 = plt.subplots(1, 1)

if __name__ == "__main__":
    sess = Inter_session(r"C:\Users\phili\_Documents\SS21\AWP\engagement_detector\logs", "Test")
    print(sess.session_paths)
