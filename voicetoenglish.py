import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import os

translator = Translator()

def record_audio(audio_file_path, duration=10):
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        print("Recording...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        audio = recognizer.listen(source, timeout=duration)

    with open(audio_file_path, "wb") as audio_file:
        audio_file.write(audio.get_wav_data())

def transcribe_translate_speak(audio_file_path, target_languages):
    recognizer = sr.Recognizer()

    for target_language in target_languages:
        try:
            with sr.AudioFile(audio_file_path) as source:
                print(f"Transcribing for {target_language}...")
                audio = recognizer.record(source)

            spoken_text = recognizer.recognize_google(audio, language=target_language)
            print(f"Transcribed text ({target_language}): {spoken_text}")

            # Translate the spoken text to English
            translation = translator.translate(spoken_text, src=target_language, dest='en')
            translated_text = translation.text

            # Speak the translated text
            tts = gTTS(text=translated_text, lang='en')
            tts.save("translated_audio.mp3")
            os.system("mpg123 translated_audio.mp3")

            # Break out of the loop after successful translation and speech
            break

        except sr.UnknownValueError:
            print(f"Could not transcribe audio for {target_language}")
        except Exception as e:
            print(f"An error occurred for {target_language}: {str(e)}")

if __name__ == "__main__":
    audio_file_path = "recorded_audio.wav"
    target_languages = ['en', 'de', 'fr', 'es', 'it']
    
    # Record audio for 10 seconds
    record_audio(audio_file_path, duration=10)
    
    # Transcribe, translate, and speak
    transcribe_translate_speak(audio_file_path, target_languages)


