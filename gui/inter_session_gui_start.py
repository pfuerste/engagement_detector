from tkinter import *
import tkinter as tk
from tkinter import ttk


class Inter_session_gui_start:
    """GUI to get start parameters

    """

    def __init__(self, lecture_names):
        """Initialize full start GUI

        Args:
            self: inter_session_gui_start class
            lecture_names (list): contains strings with known Lecture Names

        """
        self.root = Tk()
        self.root.geometry("400x250+0+0")
        self.root.title("InterSession Engagement Detector")
        self.lecture_name = ""
        self.list = lecture_names
        self.average_data = False
        self.single_data = False
        self.emotion = -1
        self.lecture_name_label = Label(
            self.root, text="Choose Lecture you want to show")
        self.lecture_name_label.place(relx=0.0, rely=0.0)
        self.lecture_name_dropdown = ttk.Combobox(self.root, values=self.list)
        self.lecture_name_dropdown.place(relx=0.6, rely=0.0)
        self.Which = Label(self.root, text="Choose how Data should be shown")
        self.Which.place(relx=0.1, rely=0.2)
        self.checkbox_average_data = tk.IntVar()
        self.average_data = Checkbutton(
            self.root,
            text="Average Data Graph",
            var=self.checkbox_average_data,
            command=self.able_average_data)
        self.average_data.place(relx=0.5, rely=0.4)
        self.checkbox_single_data = tk.IntVar()
        self.single_data = Checkbutton(
            self.root,
            text="Single Emotion Data Graph",
            var=self.checkbox_single_data,
            command=self.able_single_data)
        self.single_data.place(relx=0.5, rely=0.5)
        self.emotion_dropdown = ttk.Combobox(
            self.root,
            values=[
                "Boredom",
                "Engagement",
                "Confusion",
                "Frustration"],
            state='disabled')
        self.emotion_dropdown.place(relx=0.6, rely=0.7)

        self.start_button = Button(
            self.root,
            text="Start!",
            command=self.start,
            state='disabled')
        self.start_button.place(relx=0.5, rely=0.85)

        self.Error = Label(self.root, text="", bg="red")

        self.root.mainloop()

    def able_average_data(self):
        """change status GUI when clicked on average data checkbox

        Args:
            self: inter_session_gui_start class

        """

        if self.checkbox_average_data.get() == 1:
            self.single_data.config(state='disabled')
            self.start_button.config(state='normal')
        elif self.checkbox_average_data.get() == 0:
            self.single_data.config(state='normal')
            self.start_button.config(state='disabled')

    def able_single_data(self):
        """change status of GUI when clicked on single data checkbox

        Args:
            self: inter_session_gui_start class

        """
        if self.checkbox_single_data.get() == 1:
            self.average_data.config(state='disabled')
            self.start_button.config(state='normal')
            self.emotion_dropdown.config(state='normal')
        elif self.checkbox_single_data.get() == 0:
            self.average_data.config(state='normal')
            self.start_button.config(state='disabled')
            self.emotion_dropdown.config(state='disabled')

    def start(self):
        """check if all parameters are correct; if => destroy self.root

        Args:
            self: inter_session_gui_start class

        """
        if self.lecture_name_dropdown.get() in self.list:
            self.lecture_name = self.lecture_name_dropdown.get()
            if self.checkbox_average_data.get() == 1:
                self.average_data = True
                self.root.destroy()
            elif self.checkbox_single_data.get() == 1:
                self.single_data = True
                if self.emotion_dropdown.get() == "Boredom":
                    self.emotion = 0
                    self.root.destroy()
                elif self.emotion_dropdown.get() == "Engagement":
                    self.emotion = 1
                    self.root.destroy()
                elif self.emotion_dropdown.get() == "Confusion":
                    self.emotion = 2
                    self.root.destroy()
                elif self.emotion_dropdown.get() == "Frustration":
                    self.emotion = 3
                    self.root.destroy()
                else:
                    self.Error.config(text="Choose a Valid Emotion")
                    self.Error.place(relx=0.6, rely=0.85)
        else:
            self.Error.config(text="Choose a valid Lecture Name")
            self.Error.place(relx=0.6, rely=0.85)


def main():
    inter_session = inter_session_guiStart("a")


if __name__ == "__main__":
    main()
