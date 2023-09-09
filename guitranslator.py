#!/usr/bin/python
import tkinter as tk
from tkinter import ttk
from translate import Translator

# Function to perform language translation
def translate_text():
    source_lang = source_language.get()
    target_lang = target_language.get()
    text_to_translate = input_text.get()

    try:
        translator = Translator(from_lang=source_lang, to_lang=target_lang)
        translation = translator.translate(text_to_translate)
        translated_text.set(translation)
    except Exception as e:
        translated_text.set(f"Translation error: {str(e)}")

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
input_text = tk.Entry(root, width=40)
input_text.pack(pady=10)
translate_button = ttk.Button(root, text="Translate", command=translate_text)
translate_button.pack()

# Display Translated Text Label
translated_text = tk.StringVar()
translated_label = ttk.Label(root, text="Translated Text:")
translated_label.pack()
translated_display = ttk.Label(root, textvariable=translated_text, wraplength=400, justify="left")
translated_display.pack(pady=10)

# Start the Tkinter main loop
root.mainloop()

