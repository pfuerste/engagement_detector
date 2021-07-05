import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)
matplotlib.use('TkAgg')
from tkinter import *
import random
import time

class Application(Frame):

    def __init__(self, master=None):

        Frame.__init__(self, master)
        matplotlib.rcParams["figure.figsize"] = [6,2]
        self.data_set = [1,2,3,4,5,6]
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
            self.create_plot(self.data_set)
            self.after(1000,self.alpha)


    def create_plot(self, dataset):

        # remove old widgets
        if self.widget:
            self.widget.destroy()

        #if self.toolbar:
        #    self.toolbar.destroy()

        # create new elements

        plt = Figure(figsize=(6, 2), dpi=100)

        a = plt.add_subplot(111)
        a.plot(dataset, '-o', label="Main response(ms)")
        a.set_ylabel("milliseconds")
        a.set_title("plot")

        canvas = FigureCanvasTkAgg(plt, self)

        #self.toolbar = NavigationToolbar2Tk(canvas, self)
        #toolbar.update()

        self.widget = canvas.get_tk_widget()
        self.widget.pack(fill=BOTH)

        #self.toolbars = canvas._tkcanvas
        #self.toolbars.pack(fill=BOTH)

        # generate a random list of 6 numbers for sake of simplicity, for the next plot
        self.data_set = random.sample(range(30), 6)


def main():

    i=0
    root = Tk()
    root.wm_title("generic app")
    root.geometry("400x240+0+0")


    app = Application(master=root)
    
    app.mainloop()

main()