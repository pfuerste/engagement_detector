import matplotlib.pyplot
import numpy as np


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


# TODO plots
# intra-session

# inter-session
