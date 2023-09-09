#!/usr/bin/python
import argparse
import speech_recognition as sr
from translate import Translator
import os
import platform
import subprocess
from gtts import gTTS

# Function to perform language translation
def translate_text(text, source_lang, target_lang):
    try:
        translator = Translator(from_lang=source_lang, to_lang=target_lang)
        translation = translator.translate(text)
        return translation
    except Exception as e:
        return f"Translation error: {str(e)}"

# Function to recognize speech from audio
def recognize_speech():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Speak something...")
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Could not understand audio."
    except sr.RequestError as e:
        return f"Could not request results: {str(e)}"

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

# Create a command-line argument parser
parser = argparse.ArgumentParser(description="Translate speech between languages")

# Add arguments for the source and target languages
parser.add_argument("source_lang", type=str, help="Source language code (e.g., 'en' for English)")
parser.add_argument("target_lang", type=str, help="Target language code (e.g., 'de' for German)")

# Parse the command-line arguments
args = parser.parse_args()

# Recognize speech
recognized_text = recognize_speech()

print(f"Recognized Text: {recognized_text}")

# Translate the recognized text to the target language
translation = translate_text(recognized_text, args.source_lang, args.target_lang)

print(f"Translation: {translation}")

# Speak the translated text
speak_text(translation, args.target_lang)

