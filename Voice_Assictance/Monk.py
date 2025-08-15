import speech_recognition as sr
import pyttsx3

# Initialize recognizer and speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty("rate", 180)  # Speech speed
engine.setProperty("volume", 1.0)  # Volume level

# Speak function
def speak(text):
    engine.say(text)
    engine.runAndWait()

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

# Main loop
while True:
    if listen_for_wake_word():
        print("Jarvis is ready to take your command...")
