import sys
import threading
import tkinter as tk

import speech_recognition as sr
import pyttsx3 as tts

import json
import requests

import random

from LightManager import LightManager


class Assistant:


    def __init__(self):



        self.url = "https://api.edenai.run/v2/text/chat"
        self.headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiZTlhNTIwZmYtZmY4Mi00M2ViLTk0NzItNGZjNjU4YTFjZTJkIiwidHlwZSI6ImFwaV90b2tlbiJ9.QR7fQciG_xlWQRe2wEz9on1rmC4o3ukdoEkCZ27xB6M"}
        self.recognizer = sr.Recognizer()  # Recognizes sounds
        self.speaker = tts.init()  # Voice of assistant
        self.speaker.setProperty("rate", 150)

        self.root = tk.Tk()
        self.label = tk.Label(text="J.A.R.V.I.S.", font=("Arial", 60, "bold"))  # What shows during the application in what font and size
        self.label.pack()

        threading.Thread(target=self.run_assistant).start()

        self.root.mainloop()

        


    def run_assistant(self):
        jarvisActivated = False   # whether jarvis is active or not.
        while True:
            try:
                with sr.Microphone() as mic:
                    print("Listening for 'Jarvis' activation...")
                    self.recognizer.adjust_for_ambient_noise(mic, duration=0.5)  # Adjust for ambient noise
                    audio = self.recognizer.listen(mic, timeout=3)  # Added timeout to prevent indefinite listening
                    text = self.recognizer.recognize_google(audio)
                    text = text.lower()
                    print(f"Recognized text: {text}")



                    if "jarvis" in text:  # Activate Jarvis
                        print("Jarvis activated.")
                        self.label.config(fg="red")  # Label (text color) becomes red when Jarvis is active
                        jarvisActivated = True   # Jarvis becomes activated
                        
                        possibleGreetings = ["How can I help?", "What can I do for you?", "Yes sir, how may I assist?"]
                        greeting = random.choice(possibleGreetings)
                        self.speaker.say(greeting)
                        self.speaker.runAndWait()

                        self.recognizer.adjust_for_ambient_noise(mic, duration=0.5)
                        audio = self.recognizer.listen(mic, timeout=5)  # Listen for command
                        text = self.recognizer.recognize_google(audio)
                        text = text.lower()
                        print(f"Recognized command: {text}")


                        #===========================================================#
                        #Here starts the custom commands zone
                        #===========================================================#


                        # Define your light trigger words
                        lightSwitchTriggerWords = ["lights", "switch the lights", "switch lights", "lightswitch", "turn on the lights", "turn off the lights", "lights on", "lights off"]

                        # Check if any of the trigger words are in the text
                        if any(word in text for word in lightSwitchTriggerWords):
                            print("Switching the lights")

                            possibleAffirmations = ["Yes", "Alright", "Yes sir", "I heard you"]
                            affirmation = random.choice(possibleAffirmations)
                            self.speaker.say(f"{affirmation}, switching the lights") #speak
                            manager = LightManager()
                            manager.lightSwitch(names=manager.names[manager.user]) #switch the lights
                            self.speaker.runAndWait()  # Keep running to listen
                            
                        else:



                        #===========================================================#
                        #Here ends the custom commands zone
                        #===========================================================#

                            if text:
                                payload = {    "providers": "perplexityai",   "text": text,    "chatbot_global_action": "Act as an assistant",    "previous_history": [],    "temperature": 0.0,    "max_tokens": 150,}

                                # Handle intents directly if BasicAssistant does not have query method
                                #response = self.handle_intent(text)  # Handle the recognized command
                                
                                queryResponse = requests.post(self.url, json=payload, headers=self.headers)
                                result = json.loads(queryResponse.text)
                                response = result['perplexityai']['generated_text']

                                print(f"Assistant response: {response}")
                                if response:
                                    self.speaker.say(response)  # Speak the response
                                    self.speaker.runAndWait()  # Keep running to listen

                        self.label.config(fg="black")  # Reset label color

            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")

                #still have to implement the jarvisActivated variable
                if jarvisActivated==True:
                    possibleNotHearing = ["I could not hear you", "sorry, i don't understand", "i do not understand you"]
                    doesNotUnderstand = random.choice(possibleNotHearing)
                    self.speaker.say(f"{doesNotUnderstand}")
                    self.speaker.runAndWait()
                    jarvisActivated = False


                self.label.config(fg="black")
                continue
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")
                self.label.config(fg="black")
                continue
            except sr.WaitTimeoutError:
                print("Listening timed out while waiting for phrase to start")
                self.label.config(fg="black")
                continue
            except Exception as e:
                print(f"Error in run_assistant: {e}")
                self.label.config(fg="black")
                continue
            


    
Assistant()

#====================================================================================================
#       TO DO LIST
#====================================================================================================

#  have the summoning of jarvis and the command in the same sentence do the command
#giving lam colour as a command
#A command to close the program
#It being a seperate launchable program, launchable without vscode
#launch on startup?