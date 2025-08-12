import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import pyjokes


# Initialize the Speech Engine
# We create a function called speak that accepts a string as input. This function prints and speaks input.

def speak(text):
    print(f"Assistance: {text}")
    try :
        engine = pyttsx3.init()
        engine. say(text)
        engine.runAndWait()
    except:
        print("Speech Output Not Supported in Cloab.")
        
        
# We then create a wish_user() function to greet the user based on the current time like:
# If it’s before 12 PM, it says “Good Morning”.
# If it’s before 6 PM, it says “Good Afternoon”.
# Otherwise it says “Good Evening”.

        
        def wish_user():
            hour = int(datetime.datetime.now().hour)
            if hour < 12:
                speak("Good Morning")
            elif hour < 18 :
                speak("Good Afternoon")
            
            else:
                speak("Good Evening")              
            speak("I am your Voice assistance .How I Can I Help You Today?")
                
      
# This list helps us test how assistant will respond without needing a real voice input.          

    
# Command input function
def take_command():
    return input("You (type command): ").lower()

# Main assistant function
def run_assistance():
    while True:
        query = take_command()

        if 'wikipedia' in query:
            speak("Searching Wikipedia...")
            query = query.replace("wikipedia", "")
            try:
                result = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia")
                speak(result)
            except:
                speak("Sorry, I couldn't find anything.")

        elif 'open youtube' in query:
            speak("Opening YouTube...")
            webbrowser.open("https://www.youtube.com/")

        elif 'open google' in query:
            speak("Opening Google...")
            webbrowser.open("https://www.google.com/")
            
        elif 'chatgpt' in query:
            speak("Opening chatgpt...")
            webbrowser.open("https://chatgpt.com/?model=auto")    

        elif 'time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The current time is {strTime}")

        elif 'joke' in query:
            joke = pyjokes.get_joke()
            speak(joke)

        elif 'exit' in query:
            speak("Goodbye! Have a nice day!")
            break

        else:
            speak("Sorry, I didn't understand that. Try again.")

# Run the assistant
run_assistance()             
                
