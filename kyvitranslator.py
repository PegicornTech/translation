#!/usr/bin/python
import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from translate import Translator
from gtts import gTTS
import os
import platform
import subprocess
import speech_recognition as sr

kivy.require('2.0.0')  # Replace with your Kivy version if necessary

class LanguageTranslatorApp(App):
    def build(self):
        self.title = "Language Translator"
        self.root = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Create language selection
        lang_selection = BoxLayout(spacing=10)
        source_label = Label(text="Source Language:")
        self.source_language = Spinner(text="en", values=["en", "es", "fr", "de", "it"])
        target_label = Label(text="Target Language:")
        self.target_language = Spinner(text="es", values=["en", "es", "fr", "de", "it"])
        lang_selection.add_widget(source_label)
        lang_selection.add_widget(self.source_language)
        lang_selection.add_widget(target_label)
        lang_selection.add_widget(self.target_language)

        # Create text input and buttons
        self.input_text = TextInput(multiline=False, hint_text="Enter text to translate")
        translate_button = Button(text="Translate")
        translate_button.bind(on_press=self.translate_text)
        recognize_button = Button(text="Recognize Speech")
        recognize_button.bind(on_press=self.recognize_speech)

        # Create labels for translated text
        self.translated_text = Label(text="", size_hint_y=None, height=44)

        # Add widgets to the layout
        self.root.add_widget(lang_selection)
        self.root.add_widget(self.input_text)
        self.root.add_widget(translate_button)
        self.root.add_widget(self.translated_text)
        self.root.add_widget(recognize_button)

        return self.root

    def translate_text(self, instance):
        source_lang = self.source_language.text
        target_lang = self.target_language.text
        text_to_translate = self.input_text.text

        try:
            translator = Translator(from_lang=source_lang, to_lang=target_lang)
            translation = translator.translate(text_to_translate)
            self.translated_text.text = translation

            # Speak the translated text
            self.speak_text(translation, target_lang)
        except Exception as e:
            self.translated_text.text = f"Translation error: {str(e)}"

    def recognize_speech(self, instance):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Speak something...")
            audio = r.listen(source)

        try:
            text = r.recognize_google(audio)
            self.input_text.text = text
        except sr.UnknownValueError:
            self.input_text.text = "Could not understand audio."
        except sr.RequestError as e:
            self.input_text.text = f"Could not request results: {str(e)}"

    def speak_text(self, text, lang):
        tts = gTTS(text=text, lang=lang)

        if platform.system() == 'Darwin':
            # On macOS, use the 'say' command
            subprocess.run(['say', text])
        else:
            # On other platforms, save as an MP3 and play it
            tts.save("translation.mp3")
            os.system("mpg321 translation.mp3")

if __name__ == '__main__':
    LanguageTranslatorApp().run()

