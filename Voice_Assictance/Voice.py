import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import wikipedia
import subprocess
import os
import pywhatkit

# Initialize recognizer and text-to-speech
recognizer = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty("rate", 180)   # Speed of speech
engine.setProperty("volume", 1.0) # Volume (0.0 to 1.0)

# Speak text
def speak(text):
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

# Listen for commands
def listen():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio).lower()
        return command
    except sr.UnknownValueError:
        print("Sorry, I did not understand.")
        return ""
    except sr.RequestError:
        print("Could not request results; check your internet connection.")
        return ""

# Listen for wake word
def listen_for_wake_word():
    with sr.Microphone() as source:
        print("Listening for wake word...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio).lower()
        if "hey jarvis" in command or "hi jarvis" in command:
            speak("Wake word detected! Listening now...")
            return True
    except sr.UnknownValueError:
        print("Couldn't understand audio")
    return False

# Open Windows settings
def open_settings():
    try:
        subprocess.Popen('start ms-settings:', shell=True)
        speak("Opening Settings.")
    except Exception:
        speak("Sorry, I couldn't open Settings.")

# Close Windows settings
def close_settings():
    try:
        os.system("taskkill /f /im SystemSettings.exe")
        speak("Closing Settings.")
    except Exception:
        speak("Sorry, I couldn't close Settings.")

# Main assistant loop
def main():
    speak("Hello! I am your voice assistant.")
    
    # Wait for wake word
    while not listen_for_wake_word():
        pass
    
    # Start listening for commands
    while True:
        command = listen()
        if not command:
            continue

        speak(f"You said: {command}")

        if "time" in command:
            time_now = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"The time is {time_now}")

        elif "open google" in command or "google" in command:
            speak("Opening Google")
            webbrowser.open("https://google.com")

        elif "play music" in command or "music" in command or "song" in command or "gana" in command:
            speak("Which song do you want to play?")
            song_name = listen()
            if song_name:
                try:
                    pywhatkit.playonyt(song_name)
                    speak(f"Playing {song_name} on YouTube")
                except Exception as e:
                    speak("Sorry, I couldn't play that song.")
                    print("Error:", e)
            else:
                speak("I didn't catch the song name. Please try again.")

        elif "wikipedia" in command:
            speak("What should I search on Wikipedia?")
            topic = listen()
            if topic:
                try:
                    results = wikipedia.summary(topic, sentences=2)
                    speak(results)
                except Exception:
                    speak("Sorry, I couldn't find information on that topic.")

        elif "open settings" in command:
            open_settings()

        elif "close settings" in command:
            close_settings()

        elif "stop" in command or "exit" in command or "quit" in command:
            speak("Goodbye! Have a nice day.")
            break

        else:
            speak(f"Searching Google for {command}")
            query = command.replace(' ', '+')
            webbrowser.open(f"https://www.google.com/search?q={query}")

if __name__ == "__main__":
    main()
