import sys
import threading
import tkinter as tk

import speech_recognition as sr
import pyttsx3 as tts

from neuralintents import BasicAssistant

class Assistant:

    def __init__(self):
        self.recognizer = sr.Recognizer()  # Recognizes sounds
        self.speaker = tts.init()  # Voice of assistant
        self.speaker.setProperty("rate", 150)

        try:
            # Initialize BasicAssistant with the path to the intents.json file
            self.assistant = BasicAssistant("c:/Own code/EWS/Jarvis/intents.json")
            print("Assistant initialized.")
        except FileNotFoundError as e:
            print(f"FileNotFoundError: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"Error initializing assistant: {e}")
            sys.exit(1)

        self.root = tk.Tk()
        self.label = tk.Label(text="Jarvis", font=("Arial", 60, "bold"))  # What shows during the application in what font and size
        self.label.pack()

        threading.Thread(target=self.run_assistant).start()

        self.root.mainloop()

    def create_file(self):  # Command to create a file
        with open("somefile.txt", "w") as f:
            f.write("Type...")

    def run_assistant(self):
        while True:
            try:
                with sr.Microphone() as mic:
                    print("Listening for 'Jarvis' activation...")
                    self.recognizer.adjust_for_ambient_noise(mic, duration=0.5)  # Adjust for ambient noise
                    audio = self.recognizer.listen(mic, timeout=5)  # Added timeout to prevent indefinite listening
                    text = self.recognizer.recognize_google(audio)
                    text = text.lower()
                    print(f"Recognized text: {text}")

                    if "jarvis" in text:  # Activate Jarvis
                        print("Jarvis activated.")
                        self.label.config(fg="red")  # Label (text color) becomes red when Jarvis is active

                        self.recognizer.adjust_for_ambient_noise(mic, duration=0.5)
                        audio = self.recognizer.listen(mic, timeout=5)  # Listen for command
                        text = self.recognizer.recognize_google(audio)
                        text = text.lower()
                        print(f"Recognized command: {text}")

                        if text == "stop":  # If text is stop, say "Bye sir" and stop running
                            self.speaker.say("Bye sir")
                            self.speaker.runAndWait()
                            self.speaker.stop()
                            self.root.destroy()
                            sys.exit()
                        else:
                            if text:
                                # Handle intents directly if BasicAssistant does not have query method
                                response = self.handle_intent(text)  # Handle the recognized command
                                print(f"Assistant response: {response}")

                                if response:
                                    self.speaker.say(response)  # Speak the response
                                    self.speaker.runAndWait()  # Keep running to listen
                                    if response == "Creating a new file...":  # Custom action based on response
                                        self.create_file()
                        self.label.config(fg="black")  # Reset label color
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
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

    def handle_intent(self, command):
        # Implement logic to handle intents based on the command received
        # You should parse the command and decide the appropriate response
        # For simplicity, a basic example is shown here:
        if "hello" in command:
            return "Hello sir"
        elif "create a file" in command or "new file" in command:
            return "Creating a new file..."
        #else:
        #    return "I'm sorry, I don't understand that command."

Assistant()