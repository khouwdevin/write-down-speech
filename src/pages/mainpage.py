from tkinter import filedialog

import os
from os import path

import ttkbootstrap as ttk
from ttkbootstrap.constants import INFO, OUTLINE

import speech_recognition as sr
import moviepy.editor as mp

from mutagen.wave import WAVE
from pydub import AudioSegment

class MainPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.entry_file = ttk.StringVar()
        self.entry_des = ttk.StringVar()

        self.notifier_text = ttk.StringVar()

        self.isConvert = ttk.BooleanVar(value = False)

        self.entry_file.trace("w", self.process_button_handler)
        self.entry_des.trace("w", self.process_button_handler)

        # File Section
        ttk.Label(self, text = "File Location", font = "TimesNewRoman 14").pack(pady = 10)

        frame_file = ttk.Frame(self)
        frame_file.pack()
        frame_file.grid_columnconfigure(0, weight = 1)
        frame_file.grid_rowconfigure(0, weight = 1)

        ttk.Entry(frame_file, textvariable = self.entry_file, justify = "center", width = 80).grid(column = 1, row = 1, padx = 10)
        ttk.Button(frame_file, text = "Browse", command = lambda:self.select_dialog(0)).grid(column = 2, row = 1)

        # Destination Section

        ttk.Label(self, text = "Destination Location", font = "TimesNewRoman 14").pack(pady = 10)

        frame_des = ttk.Frame(self)
        frame_des.pack()
        frame_des.grid_columnconfigure(0, weight = 1)
        frame_des.grid_rowconfigure(0, weight = 1)

        ttk.Entry(frame_des, textvariable = self.entry_des, justify = "center", width = 80).grid(column = 1, row = 3, padx = 10)
        ttk.Button(frame_des, text = "Browse", command = lambda:self.select_dialog(1)).grid(column = 2, row = 3)

        # Process Button

        self.process_btn = ttk.Button(self, text = "Process", bootstyle=(INFO, OUTLINE), command = self.process, state = "disabled")
        self.process_btn.pack(pady = 10)

        # Notifier Section

        ttk.Label(self, textvariable = self.notifier_text, font = "TimesNewRoman 14").pack(pady = 10)

    def process_button_handler(self, *args):
        if (len(self.entry_file.get()) > 0 and len(self.entry_des.get()) > 0):
            self.process_btn.configure(state = "enabled")
        else:
            self.process_btn.configure(state = "disabled")

    def select_dialog(self, status: int):
        if (status == 0):
            self.entry_file.set(filedialog.askopenfilename(title = "Choose file", initialdir = ".", filetypes = [("All", "*.mp4 *.mp3")]))
        else:
            self.entry_des.set(filedialog.asksaveasfilename(title = "Choose directory", initialdir = ".", confirmoverwrite = True, defaultextension = "*.*", initialfile = "speech_to_text", filetypes = [("text", "*.txt")]))

    def define_audio_path(self):
        file_ext = path.splitext(path.split(self.entry_file.get())[1])
        
        if (file_ext[1] == ".mp4"):
            audio_path = path.split(self.entry_des.get())[0]

            try:
                clip = mp.VideoFileClip(self.entry_file.get())
                clip.audio.write_audiofile(path.join(audio_path, "temp.wav"))

                self.isConvert.set(True)

                self.notifier_text.set("Convert audio complete")
                return path.join(audio_path, "temp.wav")
            except OSError:
                self.notifier_text.set("File not found")
                return ""
        else:
            sound = AudioSegment.from_mp3(self.entry_file.get())
            sound.export(path.join(audio_path, "temp.wav"), format = "wav")
            return path.join(audio_path, "temp.wav")

    def process(self):
        audio_path = self.define_audio_path()
        recognizer = sr.Recognizer()

        if (len(audio_path) > 0):
            audio = sr.AudioFile(audio_path)

            duration = int(WAVE(audio_path).info.length)

            for i in range(0, int(duration), 60):
                if (i+60) >= int(duration):
                    with audio as source:
                        audio_file = recognizer.record(source, duration = 60, offset = i)
                        result = recognizer.recognize_google(audio_file, language = "id")
                        print(result)
                else:
                    rest = int(duration) - i
                    with audio as source:
                        audio_file = recognizer.record(source, duration = rest, offset = i)
                        result = recognizer.recognize_google(audio_file, language = "id")
                        print(result)

            if (self.isConvert.get()):
                os.remove(audio_path)

            self.notifier_text.set("Process is done")

            self.entry_file.set("")
            self.entry_des.set("")
            self.isConvert.set(False)
