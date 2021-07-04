import matplotlib.pyplot


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

    def append_data(self, new_data):
        for i, emo_data in enumerate(new_data):
            self.data[i].append(emo_data)
        self.append_averages(new_data)

    def append_averages(self, new_data):
        new_averages = [sum(l)/len(l) for l in new_data]
        self.avg_boredom.append(new_averages[0])
        self.avg_engagement.append(new_averages[1])
        self.avg_confusion.append(new_averages[2])
        self.avg_frustration.append(new_averages[3])

    def current_avgs(self):
        return self.avg_boredom[-1], self.avg_engagement[-1], \
               self.avg_confusion[-1], self.avg_frustration[-1]



# TODO plots
# intra-session


def averages_in_time(lists):
    pass
# inter-session
