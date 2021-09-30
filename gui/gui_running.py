from tkinter import *


class Application(Frame):
    """Frame/GUI for running program"""

    def __init__(self, master=None):
        self.end_run = False
        Frame.__init__(self, master)
        self.initUI()
        # to assign widgets
        self.widget = None
        self.toolbar = None

    def initUI(self):
        """pack quit button on Frame

        Args:
            self: Application(Frame)

        """
        self.pack(fill=BOTH, expand=1)
        quit_button = Button(
            self,
            text="Quit",
            command=self.send,
            height=2,
            width=40)
        quit_button.pack(side=TOP)

    def get_end(self):
        """Return if programm should be stopped

        Args:
            self: Application(Frame)

        Returns:
            end_run (bool): current status
        """
        return self.end_run

    def send(self):
        """Preparing end of program and close Frame

        Args:
            self: Application(Frame)

        """
        self.end_run = True
        print("Will close shortly.")
        self.quit()

    def window_warning(self, text):
        """Adds warning message to frame

        Args:
            self: Application(Frame)
            text (str) : warning message

        """
        warning = Label(self, text=text, bg="red")
        warning.pack(side=TOP)
        self.after(10000, warning.pack_forget)

    def intra_avg_plot(self, vis_data):
        """Updating plot with new data

        Args:
            self: Application(Frame)
            vis_data: contains live data

        """
        vis_data.get_avg_plots(window=self)
        self.update()

    def inter_avg_plot(self, session_data):
        """Loading plot with average data from specific session

        Args:
            self: Application(Frame)
            session_data: contains specific session

        """
        session_data.get_avg_plots(window=self)
        self.update()

    def inter_emo_plot(self, session_data, emo_id):
        """Loading emotion plot from specific session

        Args:
            self: Application(Frame)
            session_data: contains specific session
            emo_id (int): contains specific emotion

        """
        session_data.get_emotion_plot(self, emo_id)
        self.update()
