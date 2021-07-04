import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)

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
        print(self.data)
        print(self.avg_boredom)
        print(self.avg_frustration)

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

    def get_avg_plots(self, window):
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

        canvas = FigureCanvasTkAgg(fig, master=window)
        canvas.draw()
        canvas.get_tk_widget().pack()
        toolbar = NavigationToolbar2Tk(canvas, window)
        toolbar.update()
        canvas.get_tk_widget().pack()
        #self.fig_avg = fig
        #self.ax0_avg = ax0
        #self.ax1_avg = ax1
        #plt.close()
        #print(type(fig))
        #plt.show()

    def get_avg_plots(self):
        fig, ax0, ax1 = self.fig_avg, self.ax0_avg, self.ax1_avg
        return fig, ax0, ax1

    def test_fig(self):
        fig, ax0, ax1 = self.get_avg_plots()
        #fig.canvas.draw()
        #plt.show()
        #fig.show()
        fig.show(fig)

# TODO plots
# intra-session

# inter-session
