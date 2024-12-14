from time import sleep
import speech_recognition as sr
import playsound3 as playsound
from gtts import gTTS
import datetime
import ctypes
import pyjokes
import subprocess
import winshell
import webbrowser
import os
from googleapiclient.discovery import build

def greet():
    hour = int(datetime.datetime.now().hour)
    if hour >= 6 and hour < 12:
        speak("Good Morning Boss!")

    elif hour >= 12 and hour < 18:
        speak("Good Afternoon Boss!")

    elif hour >= 18 and hour < 21:
        speak("Good Evening Boss!")

    else:
        speak("Good Night Boss!")

def set_language():
    speak("Please tell me the language you prefer.")
    while True:
        lang_query = listen().lower()
        if lang_query:
            if "english" in lang_query:
                return "en", "ga" # English, Irish accent (modify as needed)
            elif "french" in lang_query:
                return "fr", "fr"  # French, France accent
            elif "spanish" in lang_query:
                return "es", "es" # Spanish, Spain accent
            elif "hindi" in lang_query:
                return "hi", "in" # Hindi, India accent
            elif "german" in lang_query:
                return "de", "de"
            elif "italian" in lang_query:
                return "it", "it"
            elif "portuguese" in lang_query:
                return "pt", "br"
            elif "mandarian chinese" in lang_query:
                return "zh-CN", "zh-CN"
            elif "korean" in lang_query:
                return "ko", "ko"
            elif "japanese" in lang_query:
                return "ja", "ja"
            elif "russian" in lang_query:
                return "ru", "ru"
            else:
                speak("I didn't understand. Please say English, French, Spanish, etc.")
        else:
            speak("I didn't hear anything. Please say your preferred language.")

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio).lower()
        print(f"You said: {text}")
        return text
    
    except sr.UnknownValueError:
        print("Could not understand audio")
        return None
    
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return None

def speak(text, language='en', accent="ga"): #irish accent
    tts = gTTS(text=text, lang=language, tld=accent)
    tts.save("response.mp3")
    playsound.playsound("response.mp3") # Use playsound
    os.remove("response.mp3")


def search_google(query):
    service = build("customsearch", "v1", developerKey="AIzaSyCxcaDScEDXEitBVIo8jbVIGVhlLoxFXUQ")
    res = service.cse().list(q=query, cx="f4fd9179accfe4e78").execute()
    try:
        return res['items'][0]['snippet']
    except:
        return "No results found."

if __name__ == "__main__":
    speak("I am Friday.  Let's set up your language preference first. Please select any one options below.")
    print("English\nFrench\nSpanish\nHindi\nGerman\nItalian\nPortuguese\nMandarin Chinese\nKorean\nJapanese\nRussian")
    current_language, current_accent = set_language()
    speak("Language set!", language=current_language, accent=current_accent)
    greet()


    while True:
        print("Listening...")
        query = listen().lower()
        if query:
            if "what is your name" or "who are you" in query:
                speak("Boss, I am FRIDAY. Your assistant")
                break

            elif "change language" in query:
                current_language, current_accent = set_language()
                speak("Language changed!", language=current_language, accent=current_accent)
                break

            elif "search" in query:
                speak("Searching...")
                query = listen()
                response = search_google(query)
                speak("Boss, according to google," + response)
                print("Boss, according to google," + response)
                query = query.replace("search", "")
                break

            elif 'open google lens' in query:
                speak("Opening Google Lens in your browser.")
                webbrowser.open("https://lens.google.com/")
                query = query.replace("open google lens", "")
                break

            elif "play" in query:
                query = query.replace("play", "")		 
                webbrowser.open(query) 
                break

            elif "open youtube" in query:
                speak("Opening Youtube")
                webbrowser.open("www.youtube.com")
                query = query.replace("open youtube", "")
                break

            elif 'open facebook' in query:
                speak("Opening Facebook")
                webbrowser.open("www.facebook.com")
                query = query.replace("open facebook", "")
                break
            
            elif 'what is the time' in query:
                speak("Boss, It's" + str(datetime.datetime.now().strftime("%H:%M")))
                query = query.replace("what is the time", "")
                break

            elif 'empty recycle bin' in query:
                speak("Emptying recycle bin")
                winshell.recycle_bin().empty(confirm = False, show_progress = False, sound = True)
                speak("Recycle bin emptied")
                query = query.replace("empty recycle bin", "")
                break

            elif 'lock window' in query:
                speak("locking the device")
                ctypes.windll.user32.LockWorkStation()
                query = query.replace("lock window", "")
                break

            elif 'shutdown system' in query:
                speak("Hold On a Sec ! Your system is on its way to shut down")
                subprocess.call('shutdown / p /f')
                query = query.replace("shutdown system", "")
                break

            elif 'how are you' in query:
                speak("I am fine, Thank you")
                speak("How are you, Sir")
                query = query.replace("how are you", "")
                break

            elif 'crack a joke' in query:
                speak(pyjokes.get_joke())
                query = query.replace("crack a joke", "")
                break
            
            elif 'exit' in query:
                speak("Logging out")
                sleep(1)
                exit()
                query = query.replace("exit", "")
                break

            else: # Default response uses current language
                speak("I didn't understand your request.", language=current_language)
                break
