from tkinter import *
import tkinter as tk
from tkinter import ttk

class inter_session_guiStart:
    def __init__(self, lecture_names):
        self.root = Tk()
        self.root.geometry("400x250+0+0")
        self.root.title("InterSession Engagement Detector")
        self.LectureName=""
        self.list=lecture_names
        self.averagedata=False
        self.singledata=False
        self.emotion=-1
        self.LectureNameLabel = Label(self.root,text="Choose Lecture you want to show")
        self.LectureNameLabel.place(relx=0.0,rely=0.0)
        self.LectureNameDropdown=ttk.Combobox(self.root,values=self.list)
        self.LectureNameDropdown.place(relx=0.6,rely=0.0)
        self.Which = Label(self.root, text="Choose how Data should be shown")
        self.Which.place(relx=0.1,rely=0.2)
        self.checkboxAverageData = tk.IntVar()
        self.AverageData = Checkbutton(
            self.root,
            text="Average Data Graph",
            var=self.checkboxAverageData,
            command=self.ableAverageData)
        self.AverageData.place(relx=0.5, rely=0.4)
        self.checkboxSingleData = tk.IntVar()
        self.SingleData = Checkbutton(
            self.root,
            text="Single Emotion Data Graph",
            var=self.checkboxSingleData,
            command=self.ableSingleData)
        self.SingleData.place(relx=0.5, rely=0.5)
        self.EmotionDropdown=ttk.Combobox(self.root,values=["Boredom","Engagement","Confusion","Frustration"],state='disabled')
        self.EmotionDropdown.place(relx=0.6,rely=0.7)


        self.StartButton = Button(self.root,text="Start!", command=self.start,state='disabled')
        self.StartButton.place(relx=0.5,rely=0.85)

        self.Error = Label(self.root,text="",bg="red")
        

        self.root.mainloop()
        
    def ableAverageData(self):
        if self.checkboxAverageData.get()==1:
            self.SingleData.config(state='disabled')
            self.StartButton.config(state='normal')
        elif self.checkboxAverageData.get()==0:
            self.SingleData.config(state='normal')
            self.StartButton.config(state='disabled')

    def ableSingleData(self):
        if self.checkboxSingleData.get()==1:
            self.AverageData.config(state='disabled')
            self.StartButton.config(state='normal')
            self.EmotionDropdown.config(state='normal')
        elif self.checkboxSingleData.get()==0:
            self.AverageData.config(state='normal')
            self.StartButton.config(state='disabled')
            self.EmotionDropdown.config(state='disabled')

    def start(self):
        self.LectureName=self.LectureNameDropdown.get()
        if self.checkboxAverageData.get()==1:
            self.averagedata=True
            self.root.destroy()
        elif self.checkboxSingleData.get()==1:
            self.singledata=True
            if self.EmotionDropdown.get()=="Boredom":
                self.emotion=0
                self.root.destroy()
            elif self.EmotionDropdown.get()=="Engagement":
                self.emotion=1
                self.root.destroy()
            elif self.EmotionDropdown.get()=="Confusion":
                self.emotion=2
                self.root.destroy()
            elif self.EmotionDropdown.get()=="Frustration":
                self.emotion=3
                self.root.destroy()
            else:
                self.Error.config(text="Choose a Valid Emotion")
                self.Error.place(relx=0.6,rely=0.85)


def main():
    inter_session = inter_session_guiStart("a")



if __name__ == "__main__":
    main()