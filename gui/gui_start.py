from tkinter import *
from tkinter import ttk
import tkinter as tk
import time
import pygetwindow


class gui_start:
    """GUI to get start parameters

    """

    def __init__(self, lecture_names):
        """Initialize full start GUI

        Args:
            self: gui_start class
            lecture_names (list): contains strings with known Lecture Names

        """
        self.root = Tk()
        self.root.title("Engagement Detector")
        self.root.geometry("360x340")
        self.lecture_name = ""
        self.input_method = ""
        self.window_name = ""
        self.duration = 90
        self.window_list = [
            name for name in pygetwindow.getAllTitles() if name is not ""]
        self.performance_mode = False
        self.lecture_name_label = Label(self.root, text="Lecture Name: ")
        self.lecture_name_label.place(x=20, y=20)
        self.list = lecture_names
        self.lecture_name_dropdown = ttk.Combobox(self.root, values=self.list)
        self.lecture_name_dropdown.place(x=160, y=20)
        self.duration_label = Label(self.root, text="Duration in minutes: ")
        self.duration_label.place(x=20, y=60)
        self.duration_entry = Entry(self.root)
        self.duration_entry.place(x=160, y=60)
        self.duration_entry.insert(0, "90")
        self.input_method_label = Label(self.root, text="Input Method")
        self.input_method_label.place(x=20, y=100)
        self.checkbox_window_grab = tk.IntVar()
        self.window_grab_tick = Checkbutton(
            self.root,
            text="Windowgrab",
            var=self.checkbox_window_grab,
            command=self.able_window_grab)
        self.window_grab_tick.place(x=60, y=140)
        self.window_name_label = Label(self.root, text="Choose Window ")
        self.window_name_label.place(x=60, y=180)
        self.window_name_dropdown = ttk.Combobox(
            self.root, values=self.window_list, state='disabled')
        self.window_name_dropdown.place(x=160, y=180)
        self.checkbox_screenshot = tk.IntVar()
        self.screenshot_tick = Checkbutton(
            self.root,
            text="Screenshot",
            var=self.checkbox_screenshot,
            command=self.able_screenshot)
        self.screenshot_tick.place(x=60, y=260)
        self.checkbox_performance = tk.IntVar()
        self.performance_tick = Checkbutton(
            self.root,
            text="Performance Mode",
            var=self.checkbox_performance)
        self.performance_tick.place(x=20, y=300)
        self.start_button = Button(
            self.root,
            text="Start!",
            command=self.start,
            state='disabled')
        self.start_button.place(x=270, y=300)
        self.error = Label(self.root, text="", bg="red")
        self.root.mainloop()

    def start(self):
        """check if all parameters are correct; if => destroy self.root

        Args:
            self: gui_start class

        """
        if (self.lecture_name_dropdown.get().strip() != ""):
            if(not any(not (c.isalnum() or c == " ") for c in self.lecture_name_dropdown.get())):
                self.lecture_name = self.lecture_name_dropdown.get().strip()
                if (self.duration_entry.get().isdigit()
                        and int(self.duration_entry.get()) > 0):
                    self.duration = int(self.duration_entry.get())
                    if self.checkbox_performance.get() == 1:
                        self.performance_mode = True
                    if self.checkbox_window_grab.get() == 1:
                        self.input_method = "window_grab"
                        if self.window_name_dropdown.get() in self.window_list:
                            self.window_name = self.window_name_dropdown.get()
                            self.root.destroy()
                        else:
                            self.error.config(text="Choose a valid Window")
                            self.error.place(x=160, y=260)
                    elif self.checkbox_screenshot.get() == 1:
                        self.input_method = "ScreenShot"
                        self.root.destroy()
                else:
                    self.error.config(text="Choose a valid duration")
                    self.error.place(x=160, y=260)
            else:
                self.error.config(text="Only Isanum&Space as Lecture")
                self.error.place(x=160, y=260)
        else:
            self.error.config(text="Enter a Lecture")
            self.error.place(x=160, y=260)

    def able_window_grab(self):
        """change status of GUI when clicked on window grab checkbox

        Args:
            self: inter_session_gui_start class

        """
        if self.checkbox_window_grab.get() == 1:
            self.window_name_dropdown.config(state='enabled')
            self.screenshot_tick.config(state='disabled')
            self.start_button.config(state='normal')

        elif self.checkbox_window_grab.get() == 0:
            self.window_name_dropdown.config(state='disabled')
            self.screenshot_tick.config(state='normal')
            self.start_button.config(state='disabled')

    def able_screenshot(self):
        """change status of GUI when clicked on screenshot checkbox

        Args:
            self: inter_session_gui_start class

        """
        if self.checkbox_screenshot.get() == 1:
            self.window_grab_tick.config(state='disabled')
            self.start_button.config(state='normal')

        elif self.checkbox_screenshot.get() == 0:
            self.window_grab_tick.config(state='normal')
            self.start_button.config(state='disabled')


if __name__ == "__main__":
    start = GuiStart(["Test1", "Test2"])
