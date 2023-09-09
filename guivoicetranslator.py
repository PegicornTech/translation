#!/usr/bin/python
import tkinter as tk
from tkinter import ttk
from translate import Translator
from gtts import gTTS
import os
import platform
import subprocess
import speech_recognition as sr

# Function to perform language translation
def translate_text():
    source_lang = source_language.get()
    target_lang = target_language.get()
    text_to_translate = input_text.get()

    try:
        translator = Translator(from_lang=source_lang, to_lang=target_lang)
        translation = translator.translate(text_to_translate)
        translated_text.set(translation)
        
        # Speak the translated text
        speak_text(translation, target_lang)
    except Exception as e:
        translated_text.set(f"Translation error: {str(e)}")

# Function to recognize speech from audio
def recognize_speech():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Speak something...")
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        input_text.set(text)
    except sr.UnknownValueError:
        input_text.set("Could not understand audio.")
    except sr.RequestError as e:
        input_text.set(f"Could not request results: {str(e)}")

# Function to speak text
def speak_text(text, lang):
    tts = gTTS(text=text, lang=lang)
    
    if platform.system() == 'Darwin':
        # On macOS, use the 'say' command
        subprocess.run(['say', text])
    else:
        # On other platforms, save as an MP3 and play it
        tts.save("translation.mp3")
        os.system("mpg321 translation.mp3")

# Create the main Tkinter window
root = tk.Tk()
root.title("Language Translator")

# Create a frame for language selection
language_frame = ttk.Frame(root)
language_frame.pack(pady=20)

# Source Language Label and Dropdown
source_label = ttk.Label(language_frame, text="Source Language:")
source_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
source_language = ttk.Combobox(language_frame, values=["en", "es", "fr", "de", "it"])
source_language.grid(row=0, column=1, padx=10, pady=5)
source_language.set("en")  # Default to English

# Target Language Label and Dropdown
target_label = ttk.Label(language_frame, text="Target Language:")
target_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
target_language = ttk.Combobox(language_frame, values=["en", "es", "fr", "de", "it"])
target_language.grid(row=1, column=1, padx=10, pady=5)
target_language.set("es")  # Default to Spanish

# Text Entry and Translation Button
input_text = tk.StringVar()
input_entry = ttk.Entry(root, textvariable=input_text, width=40)
input_entry.pack(pady=10)
translate_button = ttk.Button(root, text="Translate", command=translate_text)
translate_button.pack()

# Display Translated Text Labels
translated_text = tk.StringVar()
translated_label = ttk.Label(root, text="Translated Text:")
translated_label.pack()
translated_display = ttk.Label(root, textvariable=translated_text, wraplength=400, justify="left")
translated_display.pack(pady=10)

# Recognize Speech Button
recognize_button = ttk.Button(root, text="Recognize Speech", command=recognize_speech)
recognize_button.pack()

# Start the Tkinter main loop
root.mainloop()

