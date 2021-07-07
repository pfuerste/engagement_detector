import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)
from tkinter import *
import sys, os
sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('.'))
from io_utils.persistence import get_sorted_session_paths, load_last_session, load_all_sessions


class vis_data():
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
        for t in range(len(data[0])):
            self.avg_boredom.append(sum([x for x in data[0][t] if x != -1]) /
                                    len([x for x in data[0][t] if x != -1]))
            self.avg_engagement.append(sum([x for x in data[1][t] if x != -1]) /
                                       len([x for x in data[1][t] if x != -1]))
            self.avg_confusion.append(sum([x for x in data[2][t] if x != -1]) /
                                      len([x for x in data[2][t] if x != -1]))
            self.avg_frustration.append(sum([x for x in data[3][t] if x != -1]) /
                                        len([x for x in data[3][t] if x != -1]))

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

    # intra-session plotting
    def get_avg_plots(self, window):
        # TODO "Alarm" for slackers
        if window.widget:
            print("destroyed")
            window.widget.destroy()

        # break if used without data
        if not self.avg_boredom:
            fig, (ax0, ax1) = plt.subplots(2, 1)
        else:
            fig, (ax0, ax1) = plt.subplots(2, 1)
            ax0.set_ylim(-1, 4)
            ax0.bar(x=["Boredom", "Engagement", "Confusion", "Frustration"],
                    height=self.current_avgs(),
                    color=["black", "green", "purple", "red"])

            ax1.set_ylim(-1, 4)
            ax1.grid()
            ax1.plot(self.avg_boredom, c="black")
            ax1.plot(self.avg_engagement, c="green")
            ax1.plot(self.avg_confusion, c="purple")
            ax1.plot(self.avg_frustration, c="red")
        # plt.show()
        canvas = FigureCanvasTkAgg(fig, master=window.root)
        # canvas.draw()
        window.widget = canvas.get_tk_widget()
        window.widget.pack(fill=BOTH)
        #toolbar = NavigationToolbar2Tk(canvas, window)
        # toolbar.update()
        # canvas.get_tk_widget().pack()
        #self.fig_avg = fig
        #self.ax0_avg = ax0
        #self.ax1_avg = ax1
        # plt.close()
        # print(type(fig))
        # plt.show()


# inter-session plotting
class inter_session():

    def __init__(self, log_dir, lecture_name):
        self.sessions_data = load_all_sessions(log_dir, lecture_name, True)
        self.sessions_vis_data = []
        self.avg_boredom = []
        self.avg_engagement = []
        self.avg_confusion = []
        self.avg_frustration = []
        for ids, scores in self.sessions_data:
            _vis_data = vis_data()
            _vis_data.reload_old_data(scores)
            self.sessions.vis_data.append(_vis_data)
        for vis_data in self.sessions_vis_data:
            self.avg_boredom.extend(vis_data.avg_boredom)
            self.avg_engagement.extend(vis_data.avg_engagement)
            self.avg_confusion.extend(vis_data.avg_confusion)
            self.avg_frustration.extend(vis_data.avg_frustration)

    def get_avg_plots():
        pass

if __name__ == "__main__":
    sess = inter_session(r"C:\Users\phili\_Documents\SS21\AWP\engagement_detector\logs", "Test")
    print(sess.session_paths)
