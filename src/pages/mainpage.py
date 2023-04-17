from tkinter import filedialog

from os import path

import ttkbootstrap as ttk
from ttkbootstrap.constants import INFO, OUTLINE

class MainPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.entry_file = ttk.StringVar()
        self.entry_des = ttk.StringVar()

        # File Section
        ttk.Label(self, text ="File Location", font = "TimesNewRoman 14").pack(pady = 10)

        frame_file = ttk.Frame(self)
        frame_file.pack()
        frame_file.grid_columnconfigure(0, weight = 1)
        frame_file.grid_rowconfigure(0, weight = 1)

        ttk.Entry(frame_file, textvariable = self.entry_file, justify = "center", width = 80).grid(column = 1, row = 1, padx = 10)
        ttk.Button(frame_file, text = "Browse", command = self.select_file).grid(column = 2, row = 1)

        # Destination Section

        ttk.Label(self, text ="Destination Location", font = "TimesNewRoman 14").pack(pady = 10)

        frame_des = ttk.Frame(self)
        frame_des.pack()
        frame_des.grid_columnconfigure(0, weight = 1)
        frame_des.grid_rowconfigure(0, weight = 1)

        ttk.Entry(frame_des, textvariable = self.entry_des, justify = "center", width = 80).grid(column = 1, row = 3, padx = 10)
        ttk.Button(frame_des, text = "Browse", command = self.select_des).grid(column = 2, row = 3)

        # Process Button

        ttk.Button(self, text = "Process", bootstyle=(INFO, OUTLINE), command = self.process).pack(pady = 10)

    def select_file(self):
        self.entry_file.set(filedialog.askopenfilename(title = "Choose file", initialdir = ".", filetypes = [("All", "*.mp4 *.mp3")]))

    def select_des(self):
        self.entry_des.set(filedialog.asksaveasfilename(title = "Choose directory", initialdir = ".", confirmoverwrite = True, defaultextension = "*.*", filetypes = [("text", "*.txt")]))

    def process(self):
        print("Process")

        self.entry_file.set("")
        self.entry_des.set("")
