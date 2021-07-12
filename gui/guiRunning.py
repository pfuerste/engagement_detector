from tkinter import *


class Application(Frame):

    def __init__(self, master=None):
        self.ende = False
        Frame.__init__(self, master)
        self.initUI()
        # to assign widgets
        self.widget = None
        self.toolbar = None

    def getEnde(self):
        return self.ende

    def Sende(self):
        self.ende = True
        print("Will close shortly.")
        self.quit()

    def initUI(self):
        self.pack(fill=BOTH, expand=1)
        quitbutton = Button(self, text="Quit", command=self.Sende, height=2, width=40)
        quitbutton.pack(side=TOP)

    def WindowWarning(self):
        warning = Label(self, text="WindowWarning", bg="red")
        warning.pack(side=TOP)
        self.after(10000, warning.pack_forget)

    def intra_avg_plot(self, vis_data):
        vis_data.get_avg_plots(window=self)
        self.update()

    def inter_avg_plot(self, session_data):
        session_data.get_avg_plots(window=self)
        self.update()

    def inter_emo_plot(self, session_data, emo_id):
        session_data.get_emotion_plot(self, emo_id)
        self.update()
