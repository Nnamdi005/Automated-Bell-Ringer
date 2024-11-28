import pyttsx3 as tts

engine = tts.init()
voices = engine.getProperty('voices')

for voice in voices:
    print(f"ID: {voice.id}, Name: {voice.name}, Lang: {voice.languages}")
