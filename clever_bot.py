# clever_bot.py

import random
import os
from playsound import playsound
from googletrans import Translator
from gtts import gTTS
import speech_recognition as sr
import threading
import tkinter as tk
from PIL import Image, ImageTk
from itertools import count
from cleverbotfree import Cleverbot


class VoiceAssistant:
    def __init__(self):
        self.translator = Translator()
        self.recognizer = sr.Recognizer()
        self.stop_gif = False

    def listen(self):
        with sr.Microphone() as source:
            audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
            try:
                text = self.recognizer.recognize_google(audio, language='tr-TR')
            except sr.UnknownValueError:
                self.speak("Üzgünüm, anlayamadım. Lütfen tekrar edin.")
                text = ""
            return text

    def speak(self, message):
        self.stop_gif = False
        tts = gTTS(text=message, lang='tr')
        filename = f"audio_{random.randint(1, 1000)}.mp3"
        tts.save(filename)
        playsound(filename)
        os.remove(filename)
        self.stop_gif = True

    def translate(self, text, dest_language):
        translated = self.translator.translate(text, dest=dest_language).text
        print(f"Translated to {dest_language}: {translated}")
        return translated

    def run_chat(self):
        with Cleverbot() as bot:
            while True:
                user_input = self.listen()
                if user_input.lower() in ["çıkış", "exit"]:
                    break
                user_input_en = self.translate(user_input, 'en')
                response = bot.single_exchange(user_input_en)
                response_tr = self.translate(response, 'tr')
                self.speak(response_tr)


class AnimatedLabel(tk.Label):
    def load(self, im_path):
        self.frames = [ImageTk.PhotoImage(img) for img in self._load_frames(im_path)]
        self.loc = 0
        self.delay = self.frames[0].info['duration']
        self.show_frame()

    def _load_frames(self, im_path):
        img = Image.open(im_path)
        frames = []
        try:
            while True:
                frames.append(img.copy())
                img.seek(len(frames))
        except EOFError:
            pass
        return frames

    def show_frame(self):
        if self.frames:
            self.config(image=self.frames[self.loc])
            self.loc = (self.loc + 1) % len(self.frames)
            self.after(self.delay, self.show_frame)


def start_gui():
    root = tk.Tk()
    lbl = AnimatedLabel(root)
    lbl.pack()
    lbl.load("bot.gif")
    root.mainloop()


def main():
    assistant = VoiceAssistant()
    gif_thread = threading.Thread(target=start_gui)
    bot_thread = threading.Thread(target=assistant.run_chat)

    gif_thread.start()
    bot_thread.start()

    gif_thread.join()
    bot_thread.join()


if __name__ == "__main__":
    main()
