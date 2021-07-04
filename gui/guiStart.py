from tkinter import *
from tkinter import ttk
import tkinter as tk
import time


class guiStart:

    def __init__(self):
        self.root = Tk()
        self.root.title("Engagement Detector")
        self.root.geometry("400x300")
        self.LectureName=""
        self.RoomName=""
        self.BrowserName=""
        self.LectureNameLabel = Label(self.root, text="Lecture Name: ")
        self.LectureNameLabel.place(x=20, y=20)
        self.LectureNameEntry = Entry(self.root)
        self.LectureNameEntry.place(x=160, y=20)
        self.InputMethodLabel = Label(self.root, text="Input Method")
        self.InputMethodLabel.place(x=20, y=60)
        self.checkboxWindowgrab = tk.IntVar()
        self.WindowGrabTick = Checkbutton(
            self.root,
            text="Windowgrab",
            var=self.checkboxWindowgrab,
            command=self.ableWindowgrab)
        self.WindowGrabTick.place(x=60, y=100)
        self.BrowserLabel = Label(self.root, text="Browser")
        self.BrowserLabel.place(x=60, y=140)
        self.BrowserDropDown = ttk.Combobox(
            self.root,
            values=[
                "Google Chrome",
                "Microsoft Edge",
                "Mozilla Firefox"],
            state='disabled')
        self.BrowserDropDown.place(x=160, y=140)
        self.RoomNameLabel = Label(self.root, text="Room Name")
        self.RoomNameLabel.place(x=60, y=180)
        self.RoomNameEntry = Entry(self.root, state='disabled')
        self.RoomNameEntry.place(x=160, y=180)
        self.checkboxScreenshot = tk.IntVar()
        self.ScreenshotTick = Checkbutton(
            self.root,
            text="Screenshot",
            var=self.checkboxScreenshot,
            command=self.ableScreenshot)
        self.ScreenshotTick.place(x=60, y=220)
        self.checkboxPerformance = tk.IntVar()
        self.PerformanceTick = Checkbutton(
            self.root,
            text="Performance Mode",
            var=self.checkboxPerformance)
        self.PerformanceTick.place(x=20, y=260)
        self.StartButton = Button(
            self.root,
            text="Start!",
            command=self.start,
            state='disabled')
        self.StartButton.place(x=300, y=250)
        self.root.mainloop()

    def start(self):
        if self.checkboxWindowgrab.get() == 1:
            if self.checkboxPerformance.get() == 1:
                self.LectureName = self.LectureNameEntry.get()
                self.RoomName = self.RoomNameEntry.get()
                self.BrowserName = self.BrowserDropDown.get()
                # print("WindowGrab Performance Modus starten")
            else:
                self.LectureName = self.LectureNameEntry.get()
                self.RoomName = self.RoomNameEntry.get()
                self.BrowserName = self.BrowserDropDown.get()
                # print("WindowGrab Modus starten")

        elif self.checkboxScreenshot.get() == 1:
            if self.checkboxPerformance.get() == 1:
                self.LectureName = self.LectureNameEntry.get()
                # print("Screenshot Performance Modus starten")

            else:
                self.LectureName = self.LectureNameEntry.get()
                # print("Screenshot Modus starten")
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


if name=="main":
    start = guiStart()
