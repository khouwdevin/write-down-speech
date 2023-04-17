from tkinter import filedialog

from os import path
import contextlib
import wave

import ttkbootstrap as ttk
from ttkbootstrap.constants import INFO, OUTLINE

import speech_recognition as sr
import moviepy.editor as mp

class MainPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.entry_file = ttk.StringVar()
        self.entry_des = ttk.StringVar()

        self.process_btn_state = ttk.StringVar()

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
        ttk.Button(frame_des, text = "Browse", command = self.select_des, state = "disabled").grid(column = 2, row = 3)

        # Process Button

        ttk.Button(self, text = "Process", bootstyle=(INFO, OUTLINE), command = self.process).pack(pady = 10)

    def select_file(self):
        self.entry_file.set(filedialog.askopenfilename(title = "Choose file", initialdir = ".", filetypes = [("All", "*.mp4 *.mp3")]))

        if (len(self.entry_file.get()) > 0 and len(self.entry_des.get()) > 0):
            self.process_btn_state.set("enabled")
        else:
            self.process_btn_state.set("disabled")

    def select_des(self):
        self.entry_des.set(filedialog.asksaveasfilename(title = "Choose directory", initialdir = ".", confirmoverwrite = True, defaultextension = "*.*", filetypes = [("text", "*.txt")]))

        if (len(self.entry_file.get()) > 0 and len(self.entry_des.get()) > 0):
            self.process_btn_state.set("enabled")
        else:
            self.process_btn_state.set("disabled")

    def define_audio_path(self):
        file_ext = path.splitext(path.split(self.entry_file)[1])
        audio_path = path.split(path.split(self.entry_file))[0]

        if (file_ext == ".mp4"):
            try:
                clip = mp.VideoFileClip(self.entry_file.get())
                clip.audio.write_audiofile(audio_path + "temp.mp3")
            except Exception:
                print("Error")

            return audio_path + "temp.mp3"
        else:
            return self.entry_file.get()

    async def process(self):
        audio_path = self.define_audio_path()
        recognizer = sr.Recognizer()

        audio = sr.AudioFile(audio_path)

        frame = await contextlib.closing(wave.open(self.entry_file.get(), "r"))
        frames = frame.getnframes()
        rate = frame.getframerate()
        duration = frames / float(rate)

        for i in range(0, int(duration), 60):
            if (i+60) >= int(duration):
                audio_file = recognizer.record(audio, duration = 60, offset = i)
                result = recognizer.recognize_google(audio_file, language = "id")
                print(result)
            else:
                rest = (i+60) - int(duration)
                audio_file = recognizer.record(audio, duration = rest, offset = i)
                result = recognizer.recognize_google(audio_file, language = "id")
                print(result)

        self.entry_file.set("")
        self.entry_des.set("")
