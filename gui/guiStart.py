from tkinter import *
from tkinter import ttk
import tkinter as tk
import time
import pygetwindow


class guiStart:

    def __init__(self, lecture_names):
        self.root = Tk()
        self.root.title("Engagement Detector")
        self.root.geometry("360x340")
        self.LectureName = ""
        #self.RoomName = ""
        #self.BrowserName = ""
        self.InputMethod = ""
        self.WindowName = ""
        self.Duration = 90
        self.WindowList = [
            name for name in pygetwindow.getAllTitles() if name is not ""]
        self.PerformanceMode = False
        self.LectureNameLabel = Label(self.root, text="Lecture Name: ")
        self.LectureNameLabel.place(x=20, y=20)
        #self.LectureNameEntry = Entry(self.root)
        #self.LectureNameEntry.place(x=160, y=20)
        self.list = lecture_names
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
        self.WindowNameLabel = Label(self.root, text="Choose Window ")
        self.WindowNameLabel.place(x=60, y=180)
        self.WindowNameDropdown = ttk.Combobox(
            self.root, values=self.WindowList, state='disabled')
        self.WindowNameDropdown.place(x=160, y=180)
        #self.BrowserLabel = Label(self.root, text="Browser")
        #self.BrowserLabel.place(x=60, y=180)
        # self.BrowserDropDown = ttk.Combobox(
        #    self.root,
        #    values=[
        #        "Google Chrome",
        #        "Microsoft Edge",
        #        "Mozilla Firefox"],
        #    state='disabled')
        #self.BrowserDropDown.place(x=160, y=180)
        #self.RoomNameLabel = Label(self.root, text="Room Name")
        #self.RoomNameLabel.place(x=60, y=220)
        #self.RoomNameEntry = Entry(self.root, state='disabled')
        #self.RoomNameEntry.place(x=160, y=220)
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
        self.Error = Label(self.root, text="", bg="red")
        self.root.mainloop()

    def start(self):
        if (self.LectureNameDropDown.get() != ""):
            if(not any(not (c.isalnum()or c==" ") for c in self.LectureNameDropDown.get())):
                self.LectureName = self.LectureNameDropDown.get()
                if (self.DurationEntry.get().isdigit()
                        and int(self.DurationEntry.get()) > 0):
                    self.Duration = int(self.DurationEntry.get())
                    if self.checkboxPerformance.get() == 1:
                        self.PerformanceMode = True
                    if self.checkboxWindowgrab.get() == 1:
                        self.InputMethod = "WindowGrab"
                        if self.WindowNameDropdown.get() in self.WindowList:
                            self.WindowName = self.WindowNameDropdown.get()
                            self.root.destroy()
                        else:
                            self.Error.config(text="Choose a valid Window")
                            self.Error.place(x=160, y=260)
                        #self.RoomName = self.RoomNameEntry.get()
                        #self.BrowserName = self.BrowserDropDown.get()
                    elif self.checkboxScreenshot.get() == 1:
                        self.InputMethod = "ScreenShot"
                    # Aufruf der jeweiligen neuen Klasse fehlt
                    # Loeschen des alten Fensters
                        self.root.destroy()
                else:
                    self.Error.config(text="Choose a valid Duration")
                    self.Error.place(x=160, y=260)
            else:
                self.Error.config(text="Only Isanum&Space as Lecture")
                self.Error.place(x=160, y=260)
        else:
            self.Error.config(text="Enter a Lecture")
            self.Error.place(x=160, y=260)

    def ableWindowgrab(self):
        if self.checkboxWindowgrab.get() == 1:
            # self.BrowserDropDown.config(state='enabled')
            # self.RoomNameEntry.config(state='normal')
            self.WindowNameDropdown.config(state='enabled')
            self.ScreenshotTick.config(state='disabled')
            self.StartButton.config(state='normal')

        elif self.checkboxWindowgrab.get() == 0:
            # self.BrowserDropDown.config(state='disabled')
            # self.RoomNameEntry.config(state='disabled')
            self.WindowNameDropdown.config(state='disabled')
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
    start = guiStart(["Test1", "Test2"])
