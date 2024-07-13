import sys
import threading
import tkinter as tk

import speech_recognition as sr
import pyttsx3 as tts

from neuralintents import GenericAssistant

recognizer = sr.Recognizer()

while True:
    try:
        with sr.Microphone() as mic:
            recognizer.adjust_for_ambient_noise(mic, duration=0.2)
            audio = recognizer.listen(mic)
            
            text = recognizer.recognize_google(audio)
            text = text.lower()
            
            print(f"Recognized: {text}")

    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand the audio")
        recognizer = sr.Recognizer()
        continue
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        break
#    if text == ("close"):
#        print("closing")
#        quit()
#    else:
#        continue


