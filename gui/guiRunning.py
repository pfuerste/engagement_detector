from tkinter import *
# from .plots import get_avg_plots


class Application(Frame):

    def __init__(self, master=None):
        self.root = Tk()
        self.root.title("Engagement Detector")
        self.root.geometry("400x240+0+0")
        Frame.__init__(self, master)
        #matplotlib.rcParams["figure.figsize"] = [6, 2]
        #self.data_set = [1, 2, 3, 4, 5, 6]
        self.initUI()

        # to assign widgets
        self.widget = None
        self.toolbar = None

    def initUI(self):
        self.pack(fill=BOTH, expand=1)

        plotbutton = Button(self, text="Plot Data", command=self.alpha)
        plotbutton.place(relx=0.2, rely=0.9)

        quitbutton = Button(self, text="Quit", command=self.quit)
        quitbutton.place(relx=0.6, rely=0.9)

    def alpha(self):
        
        self.after(1000, self.alpha)
