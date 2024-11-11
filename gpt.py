import os
import openai
from dotenv import load_dotenv
import time
import speech_recognition as sr
import numpy as np
from gtts import gTTS

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

model = 'gpt-4-turbo'  # Specify GPT-4-turbo model
r = sr.Recognizer()
name = "Alex"
greetings = [
    f"whats up master {name}",
    "yeah?",
    "Well, hello there, Master of Puns and Jokes - how's it going today?",
    f"Ahoy there, Captain {name}! How's the ship sailing?",
    f"Bonjour, Monsieur {name}! Comment ça va? Wait, why the hell am I speaking French?"
]

# Listen for the wake word "hey"
def listen_for_wake_word(source):
    print("Listening for 'Hey'...")
    while True:
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            if "hey" in text.lower():
                print("Wake word detected.")
                speak(np.random.choice(greetings))
                listen_and_respond(source)
                break
        except sr.UnknownValueError:
            pass

# Listen for input and respond with OpenAI API
def listen_and_respond(source):
    print("Listening...")
    while True:
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            print(f"You said: {text}")
            if not text:
                continue

            # Send input to OpenAI API
            response = openai.ChatCompletion.create(
                model="gpt-4-turbo",
                messages=[{"role": "user", "content": f"{text}"}]
            )
            response_text = response.choices[0].message.content
            print(response_text)

            # Generate audio with gTTS
            if response_text:
                myobj = gTTS(text=response_text, lang='en', slow=False)
                myobj.save("response.mp3")
                print("speaking")
                os.system("omxplayer response.mp3")  # Or use vlc if preferred

            # Return to listening for the wake word after speaking
            listen_for_wake_word(source)
            break
        except sr.UnknownValueError:
            time.sleep(2)
            print("Silence found, shutting up, listening...")
            listen_for_wake_word(source)
            break
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            speak(f"Could not request results; {e}")
            listen_for_wake_word(source)
            break

def speak(text):
    myobj = gTTS(text=text, lang='en', slow=False)
    myobj.save("greeting.mp3")
    os.system("omxplayer greeting.mp3")

# Use the default microphone as the audio source
with sr.Microphone() as source:
    listen_for_wake_word(source)