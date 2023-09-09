import os
import sounddevice as sd
import numpy as np
import speech_recognition as sr
from langdetect import detect
from pydub import AudioSegment
from translate import Translator as TranslateTranslator
from gtts import gTTS

# Initialize the recognizer
recognizer = sr.Recognizer()

# Set the language recognizer to English
recognizer.energy_threshold = 4000
recognizer.dynamic_energy_threshold = True

# Record audio for 10 seconds into a buffer
def record_audio():
    with sd.InputStream(callback=audio_callback):
        sd.sleep(10000)

audio_buffer = []

def audio_callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    audio_buffer.append(indata.copy())

# Playback the audio from an audio file
def playback_audio(audio_file):
    os.system(f"mpg123 {audio_file}")

# Transcribe the audio from a WAV file
def transcribe_audio_wav(audio_file):
    try:
        with sr.AudioFile(audio_file) as source:
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio)
            return text
    except sr.UnknownValueError:
        return ""

# Convert audio to a compatible format (Mono or Stereo)
def convert_to_compatible_format(audio_data):
    if audio_data.ndim == 2 and audio_data.shape[1] > 1:  # Stereo audio
        return audio_data[:, 0]  # Use only the first channel (left channel)
    return audio_data  # Mono audio or stereo with one channel

# Translate text to English
def translate_to_english(text, source_lang):
    translator = TranslateTranslator(to_lang="en", from_lang=source_lang)
    translation = translator.translate(text)
    return translation

# Speak the translated text and save it as an audio file
def speak_text(text, output_file):
    tts = gTTS(text=text, lang="en")
    tts.save(output_file)
    playback_audio(output_file)

# Language recognition
def recognize_language(text):
    try:
        language = detect(text)
        return language
    except:
        return "unknown"

if __name__ == "__main__":
    print("Recording audio...")
    record_audio()
    
    if audio_buffer:
        print("Saving recorded audio to a temporary WAV file...")
        audio_data = np.concatenate(audio_buffer)
        audio_data = convert_to_compatible_format(audio_data)  # Convert to compatible format
        audio = AudioSegment(audio_data.tobytes(), frame_rate=44100, sample_width=audio_data.dtype.itemsize, channels=1)
        audio.export("temp_audio.wav", format="wav")
        
        print("Transcribing audio...")
        transcribed_text = transcribe_audio_wav("temp_audio.wav")
        
        if transcribed_text:
            print("Recognized Text:", transcribed_text)
            detected_language = recognize_language(transcribed_text)
            print("Detected Language:", detected_language)
            
            if detected_language != "unknown":
                translated_text = translate_to_english(transcribed_text, detected_language)
                print("Translated Text:", translated_text)
                print("Speaking translated text...")
                speak_text(translated_text, "translated.mp3")
            else:
                print("Language not recognized.")
        else:
            print("No text recognized.")
    else:
        print("No audio data recorded.")

