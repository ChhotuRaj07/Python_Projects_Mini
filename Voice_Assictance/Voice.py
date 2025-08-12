import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import wikipedia
import subprocess
import requests
from bs4 import BeautifulSoup
import os

engine = pyttsx3.init()
engine.setProperty("rate", 180)
engine.setProperty("volume", 1)

def speak(text):
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio, language='en-in')
        print(f"You said: {command}")
        return command.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn't understand. Please say that again.")
        return ""
    except sr.RequestError:
        speak("Sorry, I am unable to access the speech service right now.")
        return ""

def get_first_youtube_url(query):
    query = query.replace(' ', '+')
    url = f"https://www.youtube.com/results?search_query={query}"
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        for link in soup.find_all("a"):
            href = link.get("href")
            if href and href.startswith("/watch?v="):
                return "https://www.youtube.com" + href
    except Exception as e:
        print("Error fetching YouTube results:", e)
    return None

def open_settings():
    try:
        subprocess.Popen('start ms-settings:', shell=True)
        speak("Opening Settings.")
    except Exception:
        speak("Sorry, I couldn't open Settings.")

def close_settings():
    try:
        os.system("taskkill /f /im SystemSettings.exe")
        speak("Closing Settings.")
    except Exception:
        speak("Sorry, I couldn't close Settings.")

def main():
    speak("Hello, I am your voice assistant. How can I help you?")

    while True:
        command = listen()

        if not command:
            continue

        # Confirm command by repeating it back every time
        speak(f"You said: {command}")

        # Time
        if "time" in command:
            time_now = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"The time is {time_now}")

        # Open youtube or play music on youtube
        elif ("youtube" in command and ("open" in command or "go inside" in command)):
            # If user says "play [song] on youtube" or "play music on youtube"
            if "play" in command:
                song = command
                if "play song" in command:
                    song = command.replace("play song", "").strip()
                elif "play music" in command:
                    song = command.replace("play music", "").strip()
                else:
                    song = command.replace("play", "").replace("on youtube","").strip()

                if song:
                    speak(f"Playing {song} on YouTube.")
                    video_url = get_first_youtube_url(song)
                    if video_url:
                        webbrowser.open(video_url)
                    else:
                        speak("Sorry, I couldn't find the song on YouTube.")
                else:
                    speak("Please say the song name to play on YouTube.")
            else:
                speak("Opening YouTube.")
                webbrowser.open("https://youtube.com")

        # Play song command directly (even without youtube mentioned)
        elif "play" in command:
            song = command.replace("play", "").strip()
            if song:
                speak(f"Playing {song} on YouTube.")
                video_url = get_first_youtube_url(song)
                if video_url:
                    webbrowser.open(video_url)
                else:
                    speak("Sorry, I couldn't find the song on YouTube.")
            else:
                speak("Please say the song name to play.")

        # Open Google
        elif "open google" in command:
            speak("Opening Google.")
            webbrowser.open("https://google.com")

        # Wikipedia open and search
        elif "open wikipedia" in command:
            speak("What topic should I search on Wikipedia?")
            topic = listen()
            if topic:
                try:
                    results = wikipedia.summary(topic, sentences=2)
                    speak(results)
                except wikipedia.exceptions.DisambiguationError:
                    speak("Your query is ambiguous. Please be more specific.")
                except wikipedia.exceptions.PageError:
                    speak("Sorry, I could not find any information on that topic.")
                except Exception:
                    speak("Sorry, something went wrong with Wikipedia.")
            else:
                speak("No topic received.")

        elif "read wikipedia" in command:
            if "about" in command:
                topic = command.split("about", 1)[1].strip()
                if topic:
                    try:
                        results = wikipedia.summary(topic, sentences=2)
                        speak(results)
                    except wikipedia.exceptions.DisambiguationError:
                        speak("Your query is ambiguous. Please be more specific.")
                    except wikipedia.exceptions.PageError:
                        speak("Sorry, I could not find any information on that topic.")
                    except Exception:
                        speak("Sorry, something went wrong with Wikipedia.")
                else:
                    speak("Please specify a topic to read from Wikipedia.")
            else:
                speak("Please say 'read Wikipedia about' followed by the topic.")

        # System control commands
        elif "open settings" in command:
            open_settings()

        elif "close settings" in command:
            close_settings()

        # Exit assistant
        elif "stop" in command or "exit" in command or "quit" in command:
            speak("Goodbye! Have a nice day.")
            break

        # Fallback: search Google
        else:
            speak(f"Searching Google for {command}")
            query = command.replace(' ', '+')
            webbrowser.open(f"https://www.google.com/search?q={query}")

if __name__ == "__main__":
    main()
