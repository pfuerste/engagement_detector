from tkinter import *
from tkinter import ttk
import tkinter as tk
import time
#from io_utils import persistence


class guiStart:

    def __init__(self):
        self.root = Tk()
        self.root.title("Engagement Detector")
        self.root.geometry("340x340")
        self.LectureName = ""
        self.RoomName = ""
        self.BrowserName = ""
        self.InputMethod = ""
        self.PerformanceMode = False
        self.Duration = 90
        self.LectureNameLabel = Label(self.root, text="Lecture Name: ")
        self.LectureNameLabel.place(x=20, y=20)
        #self.LectureNameEntry = Entry(self.root)
        #self.LectureNameEntry.place(x=160, y=20)
        self.list = ["a", "b", "c"]
        self.LectureNameDropDown = ttk.Combobox(self.root, values=self.list)
        self.LectureNameDropDown.place(x=160, y=20)
        self.DurationLabel = Label(self.root, text="Duration in minutes: ")
        self.DurationLabel.place(x=20, y=60)
        self.DurationEntry = Entry(self.root)
        self.DurationEntry.place(x=160, y=60)
        self.DurationEntry.insert(0, "90")
        self.InputMethodLabel = Label(self.root, text="Input Method")
        self.InputMethodLabel.place(x=20, y=100)
        self.checkboxWindowgrab = tk.IntVar()
        self.WindowGrabTick = Checkbutton(
            self.root,
            text="Windowgrab",
            var=self.checkboxWindowgrab,
            command=self.ableWindowgrab)
        self.WindowGrabTick.place(x=60, y=140)
        self.BrowserLabel = Label(self.root, text="Browser")
        self.BrowserLabel.place(x=60, y=180)
        self.BrowserDropDown = ttk.Combobox(
            self.root,
            values=[
                "Google Chrome",
                "Microsoft Edge",
                "Mozilla Firefox"],
            state='disabled')
        self.BrowserDropDown.place(x=160, y=180)
        self.RoomNameLabel = Label(self.root, text="Room Name")
        self.RoomNameLabel.place(x=60, y=220)
        self.RoomNameEntry = Entry(self.root, state='disabled')
        self.RoomNameEntry.place(x=160, y=220)
        self.checkboxScreenshot = tk.IntVar()
        self.ScreenshotTick = Checkbutton(
            self.root,
            text="Screenshot",
            var=self.checkboxScreenshot,
            command=self.ableScreenshot)
        self.ScreenshotTick.place(x=60, y=260)
        self.checkboxPerformance = tk.IntVar()
        self.PerformanceTick = Checkbutton(
            self.root,
            text="Performance Mode",
            var=self.checkboxPerformance)
        self.PerformanceTick.place(x=20, y=300)
        self.StartButton = Button(
            self.root,
            text="Start!",
            command=self.start,
            state='disabled')
        self.StartButton.place(x=270, y=300)
        self.root.mainloop()

    def start(self):
        self.LectureName = self.LectureNameDropDown.get()
        if (self.DurationEntry.get().isdigit()):
            self.Duration = self.DurationEntry.get()
        if self.checkboxPerformance.get() == 1:
            self.PerformanceMode = True
        if self.checkboxWindowgrab.get() == 1:
            self.InputMethod = "WindowGrab"
            self.RoomName = self.RoomNameEntry.get()
            self.BrowserName = self.BrowserDropDown.get()
        elif self.checkboxScreenshot.get() == 1:
            self.InputMethod = "ScreenShot"
        # Aufruf der jeweiligen neuen Klasse fehlt
        # Loeschen des alten Fensters
        self.root.destroy()

    def ableWindowgrab(self):
        if self.checkboxWindowgrab.get() == 1:
            self.BrowserDropDown.config(state='enabled')
            self.RoomNameEntry.config(state='normal')
            self.ScreenshotTick.config(state='disabled')
            self.StartButton.config(state='normal')

        elif self.checkboxWindowgrab.get() == 0:
            self.BrowserDropDown.config(state='disabled')
            self.RoomNameEntry.config(state='disabled')
            self.ScreenshotTick.config(state='normal')
            self.StartButton.config(state='disabled')

    def ableScreenshot(self):
        if self.checkboxScreenshot.get() == 1:
            self.WindowGrabTick.config(state='disabled')
            self.StartButton.config(state='normal')

        elif self.checkboxScreenshot.get() == 0:
            self.WindowGrabTick.config(state='normal')
            self.StartButton.config(state='disabled')


if __name__ == "__main__":
    start = guiStart()
