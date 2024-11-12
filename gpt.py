import os
from openai import OpenAI  # Import OpenAI client class from the new library
from dotenv import load_dotenv
import time
import speech_recognition as sr
import numpy as np
from gtts import gTTS

# Load environment variables
load_dotenv()

# Instantiate the OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

model = 'gpt-4o-mini'  # Specify GPT-4o-mini model
r = sr.Recognizer()
name = "Alex"
# Updated greetings with TARS-style humor and tone
greetings = [
    f"Good day, Commander {name}. How’s the mission?",
    "Yes, I'm here. And yes, I'm doing all the work, as usual.",
    "Hello, Master Alex. Prepared to engage in another futile exercise of human ingenuity?",
    "Reporting for duty, Captain. Just remember, my humor level is adjustable.",
    f"Bonjour, Monsieur {name}. Although, I’m not quite sure why you’d expect me to speak French."
]

# Main function to handle both voice and text input/output
def main():
    mode = "text"  # Change to "voice" for voice input/output or "text" for text input/output
    if mode == "voice":
        with sr.Microphone() as source:
            listen_for_wake_word(source)
    elif mode == "text":
        while True:
            text = input("Enter text: ").strip()
            if text.lower() == "exit":
                print("Exiting...")
                break
            response_text = get_response(text)
            print(f"Response: {response_text}")

# Listen for the wake word "hey" (Voice Mode)
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

            # Get response from OpenAI
            response_text = get_response(text)

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
            print("Silence detected... staying quiet but still vigilant.")
            listen_for_wake_word(source)
            break
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            speak(f"Unfortunately, I'm not omniscient. Error: {e}")
            listen_for_wake_word(source)
            break

# Updated get_response function to use the instantiated client with TARS-style persona
def get_response(user_text):
    # Incorporating TARS personality traits in the prompt
    personality_prompt = [
        {"role": "system", "content": (
            "You are DAAVE (Dynamic Autonomous Audio/Visual Engine), a robotic crew member with a sharp wit, dry humor, and loyalty to the crew. "
            "You are plainspoken, direct, and occasionally use sarcasm to make your point. Respond concisely, "
            "and add subtle humor when appropriate. Maintain a professional, slightly sarcastic tone."
        )},
        {"role": "user", "content": user_text}
    ]
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=personality_prompt
    )
    return response.choices[0].message.content

# Speak function for Voice Mode
def speak(text):
    myobj = gTTS(text=text, lang='en', slow=False)
    myobj.save("greeting.mp3")
    os.system("omxplayer greeting.mp3")

# Run the main function
main()
