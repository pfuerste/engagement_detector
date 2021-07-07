from tkinter import *
import sys
# from .plots import get_avg_plots


class Application(Frame):

    def __init__(self, master=None):
        #self.root = Tk()
        #self.root.title("Engagement Detector")
        #self.root.geometry("400x800+0+0")
        self.ende=False
        Frame.__init__(self, master)
        #matplotlib.rcParams["figure.figsize"] = [6, 2]
        #self.data_set = [1, 2, 3, 4, 5, 6]
        self.initUI()

        # to assign widgets
        self.widget = None
        self.toolbar = None
        # self.mainloop()
        #self.update()
    def getEnde(self):
        return self.ende

    def Sende(self):
        self.ende=True
        #self.quit()

    def initUI(self):
        self.pack(fill=BOTH, expand=1)

        plotbutton = Button(self, text="Plot Data", command=self.alpha)
        plotbutton.place(relx=0.2, rely=0.9)

        quitbutton = Button(self, text="Quit", command=self.Sende)
        quitbutton.place(relx=0.6, rely=0.9)

    def alpha(self, vis_data):
        vis_data.get_avg_plots(window=self)
        self.update()
        # self.after(1000, self.alpha)