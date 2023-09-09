#!/bin/python
import argparse
from translate import Translator

# Function to perform language translation
def translate_text(text, source_lang, target_lang):
    try:
        translator = Translator(from_lang=source_lang, to_lang=target_lang)
        translation = translator.translate(text)
        return translation
    except Exception as e:
        return f"Translation error: {str(e)}"

# Create a command-line argument parser
parser = argparse.ArgumentParser(description="Translate text between languages")

# Add arguments for the text to translate, source language, and target language
parser.add_argument("text", type=str, help="The text to translate")
parser.add_argument("source_lang", type=str, help="Source language code (e.g., 'en' for English)")
parser.add_argument("target_lang", type=str, help="Target language code (e.g., 'de' for German)")

# Parse the command-line arguments
args = parser.parse_args()

# Translate the provided text from the source language to the target language
translation = translate_text(args.text, args.source_lang, args.target_lang)

print(f"Source Text: {args.text}")
print(f"Translation: {translation}")
