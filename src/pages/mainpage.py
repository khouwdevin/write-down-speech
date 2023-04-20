from tkinter import filedialog

from typing import List

import os
from os import path
import threading

from time import gmtime, strftime

import ttkbootstrap as ttk
from ttkbootstrap.constants import INFO, OUTLINE

import speech_recognition as sr
import moviepy.editor as mp

from mutagen.wave import WAVE
from pydub import AudioSegment

class MainPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller: ttk.Window = controller

        self.entry_file_variable = ttk.StringVar()
        self.entry_des_variable = ttk.StringVar()
        self.notifier_var = ttk.StringVar()

        self.entry_duration_variable = ttk.IntVar(value = 10)

        self.is_convert = ttk.BooleanVar(value = False)

        self.entry_file_variable.trace("w", self.process_button_handler)
        self.entry_des_variable.trace("w", self.process_button_handler)

        # File Section
        ttk.Label(self, text = "File Location", font = "TimesNewRoman 14").pack(pady = 10)

        frame_file = ttk.Frame(self)
        frame_file.pack()
        frame_file.grid_columnconfigure(0, weight = 1)
        frame_file.grid_rowconfigure(0, weight = 1)

        self.entry_file = ttk.Entry(frame_file, textvariable = self.entry_file_variable, justify = "center", width = 80)
        self.entry_file.grid(column = 1, row = 1, padx = 10)
        ttk.Button(frame_file, text = "Browse", command = lambda:self.select_dialog(0)).grid(column = 2, row = 1)

        # Destination Section

        ttk.Label(self, text = "Destination Location", font = "TimesNewRoman 14").pack(pady = 10)

        frame_des = ttk.Frame(self)
        frame_des.pack()
        frame_des.grid_columnconfigure(0, weight = 1)
        frame_des.grid_rowconfigure(0, weight = 1)

        self.entry_des = ttk.Entry(frame_des, textvariable = self.entry_des_variable, justify = "center", width = 80)
        self.entry_des.grid(column = 1, row = 3, padx = 10)
        ttk.Button(frame_des, text = "Browse", command = lambda:self.select_dialog(1)).grid(column = 2, row = 3)

        # Duration Section

        ttk.Label(self, text = "Timestamp Duration", font = "TimesNewRoman 14").pack(pady = 10)

        self.entry_duration = ttk.Entry(self, textvariable = str(self.entry_duration_variable), justify = "center", width = 80)
        self.entry_duration.pack(pady = 10)

        # Process Button

        self.process_btn = ttk.Button(self, text = "Process", bootstyle=(INFO, OUTLINE), command = lambda:threading.Thread(target = self.process).start(), state = "disabled")
        self.process_btn.pack(pady = 10)

        # Notifier Section

        ttk.Label(self, textvariable = self.notifier_var, font = "TimesNewRoman 14").pack(pady = 10)

    def process_button_handler(self, *args):
        if (len(self.entry_file_variable.get()) > 0 and len(self.entry_des_variable.get()) > 0):
            self.process_btn.configure(state = "enabled")
        else:
            self.process_btn.configure(state = "disabled")

    def select_dialog(self, status: int):
        if (status == 0):
            self.entry_file_variable.set(filedialog.askopenfilename(title = "Choose file", initialdir = ".", filetypes = [("All", "*.mp4 *.mp3")]))
        else:
            self.entry_des_variable.set(filedialog.asksaveasfilename(title = "Choose directory", initialdir = ".", confirmoverwrite = True, defaultextension = "*.*", initialfile = "speech_to_text", filetypes = [("text", "*.txt")]))
    
    def notifier_text(self, text_message):
        self.notifier_var.set(text_message)
        self.controller.update()
    
    def remove_processing(self, text, audio_path):
        if (self.is_convert.get()):
            os.remove(audio_path)

        self.notifier_text(text)

        self.entry_file_variable.set("")
        self.entry_des_variable.set("")
        self.is_convert.set(False)
        self.set_entry(False)
    
    def set_entry(self, is_active: bool):
        state_str = "disabled" if is_active else "active"

        if (is_active):
            self.process_btn.configure(state = state_str)

        self.entry_des.configure(state = state_str)
        self.entry_file.configure(state = state_str)
        self.entry_duration.configure(state = state_str)

        self.controller.update()

    def define_audio_path(self):
        file_ext = path.splitext(path.split(self.entry_file_variable.get())[1])
        
        if (file_ext[1] == ".mp4"):
            audio_path = path.split(self.entry_des_variable.get())[0]

            try:
                self.notifier_text("Converting audio...")

                clip = mp.VideoFileClip(self.entry_file_variable.get())
                clip.audio.write_audiofile(path.join(audio_path, "temp.wav"))

                self.is_convert.set(True)

                self.notifier_text("Convert audio complete")
                return path.join(audio_path, "temp.wav")
            except OSError:
                self.notifier_text("File not found")
                return ""
        else:
            self.notifier_text("Converting audio...")

            sound = AudioSegment.from_mp3(self.entry_file_variable.get())
            sound.export(path.join(audio_path, "temp.wav"), format = "wav")

            self.notifier_text("Convert audio complete")
            return path.join(audio_path, "temp.wav")

    def process(self):
        self.set_entry(True)

        audio_path = self.define_audio_path()
        record_duration = self.entry_duration_variable.get()
        recognizer = sr.Recognizer()

        result_list: List[str] = []

        if (path.exists(self.entry_des_variable.get())):
            os.remove(self.entry_des_variable.get())

        if (len(audio_path) > 0):
            audio = sr.AudioFile(audio_path)

            duration = int(WAVE(audio_path).info.length)
            
            try:
                if (path.exists(self.entry_des_variable.get())):
                    os.remove(self.entry_des_variable.get())

                if (len(audio_path) > 0):
                    audio = sr.AudioFile(audio_path)

                    duration = int(WAVE(audio_path).info.length)
                    
                    with audio as source:
                        audio_file = recognizer.record(source)

                    for i in range(0, int(duration), record_duration):
                        percentage = i / duration * 100
                        self.notifier_text(f"Processing speech to text {int(percentage)}%...")

                        if (i + record_duration) <= int(duration):
                            timestamp_before = strftime("%M:%S", gmtime(i))
                            timestamp_after = strftime("%M:%S", gmtime(i + record_duration))
                            timestamp = f"Timestamp ({timestamp_before} - {timestamp_after})"

                            current_audio = audio_file.get_segment(i * 1000, (i + record_duration) * 1000)
                            result = recognizer.recognize_google(current_audio, language = "id")

                            result_list.append(timestamp)
                            result_list.append("\n")
                            result_list.append(result)
                            result_list.append("\n\n")
                        else:
                            rest = int(duration) - i
                            timestamp_before = strftime("%M:%S", gmtime(i))
                            timestamp_after = strftime("%M:%S", gmtime(i + rest))
                            timestamp = f"Timestamp ({timestamp_before} - {timestamp_after})"

                            current_audio = audio_file.get_segment(i * 1000, (i + rest) * 1000)
                            result = recognizer.recognize_google(current_audio, language = "id")

                            result_list.append(timestamp)
                            result_list.append("\n")
                            result_list.append(result)
                            result_list.append("\n\n")

                    with open(file = self.entry_des_variable.get(), mode = "a", encoding = "utf8") as file_system:
                        for word in result_list:
                            file_system.writelines(word)

                    self.remove_processing("Processing complete", audio_path)
                    self.after(5000, lambda:self.notifier_text(""))
            except sr.RequestError:
                self.remove_processing("No internet", audio_path)
                self.after(5000, lambda:self.notifier_text(""))
            except:
                self.remove_processing("Process error, please try again", audio_path)
                self.after(5000, lambda:self.notifier_text(""))
