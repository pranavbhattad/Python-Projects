# importing modules
import pyttsx3
import datetime
from datetime import date
import speech_recognition as sr
import wikipedia
import os
import webbrowser
import pywhatkit
import pyjokes


#  voice or speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


# what is speak? defining it...
def speak(audio):
    engine.say(audio)
    engine.runAndWait()


#  Web Browser (Windows)
chrome = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
edge = 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe %s'
tdate = "today's date"


# Function WishMe...
def wishMe():
    hour = int(datetime.datetime.now().hour)

    # Sleeping Remind
    if hour >= 0 and hour < 4:
        speak("Sir it is Late Night, You should sleep")

    # Good Morning
    if hour >= 5 and hour < 12:
        speak("Good Morning Sir")

    #  Afternoon
    elif hour >= 12 and hour < 16:
        speak("Good Afternoon Sir")

    # Evening
    elif hour >= 16 and hour < 20:
        speak("Good Evening Sir")

    # Night:
    else:
        speak("Bon Nuit")

    # I am Leo... And Bla*3
    speak("I am Leo. Please tell how may I help you?")


# take command i.e input's voice
# from the user and returns output

def takeCommand():

    query = ""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 0.5
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio , language='en-in')
        print(f">>> {query}\n")

    except Exception as e:
        print(e)
        if query:
            speak("Say that again please...")

    return query


# Main Working

if __name__ == "__main__":
    
# Calling the Wish Me Function
    wishMe()

    while True:
        
        query = takeCommand().lower()

        # Logic for executing tasks based on query
        
        # WIKIPEDIA
        if 'leo' in query:
            if 'wikipedia' in query:
                speak('Searching Wikipedia...')
                query = query.replace("wikipedia", "")
                results = wikipedia.summary(query, sentences=3)
                speak("According to Wikipedia")
                print(results)
                speak(results)
            
            #  All Web relative work
            
            # Open Google 
            elif 'open google' in query:
                speak("opening google")
                webbrowser.get(chrome).open("google.com")
                
                
            # Do google Search
            elif 'search google' in query:
                speak ("searching google")
                indx = query.lower().split().index('google')
                search = query.split()[indx + 1:]
                webbrowser.get(chrome).open("https://www.google.com/search?q=" + '+'.join(search))
            

            # Bing!
            elif 'open bing' in query:
                speak("opening bing")
                webbrowser.get(edge).open("bing.com")
            

            # Open Youtube
            elif 'open youtube' in query:
                speak("opening youtube")
                webbrowser.get(chrome).open("youtube.com")
                
                
            # Do a YoutTube Search or Find Videos
            elif 'search youtube' in query:
                speak("searching youtube")
                indx = query.lower().split().index('youtube')
                search = query.split()[indx+1:]
                webbrowser.get(chrome).open("http://www.youtube.com/results?search_query=" + '+'.join(search))
            
            
            # GitHub!
            elif 'open github' in query:
                speak("opening github")
                webbrowser.get(chrome).open("github.com")
                
                
            # Twitter
            elif 'open twitter' in query:
                speak("opening twitter")
                webbrowser.get(chrome).open("twitter.com")


            # Translator
            elif 'open translator' in query:
                speak("opening translator")
                webbrowser.get(chrome).open("translate.google.com")
            
            
            #  All Music Stuff
            
            
            #  Plays the song downloaded in my PC
            elif 'music' in query:
                speak("Playing music... Enjoy Music")
                music_dir = 'F:\\Songs\\Playlist'
                gaane = os.listdir(music_dir)
                # print(songs)
                os.startfile(os.path.join(music_dir, gaane[0]))
            
            
            #  Open Soptify
            elif 'spotify' in query:
                speak ("Opening Spotify... Enjoy Music")
                spotify_path = "C:/Users/PRANAV BHATTAD/AppData/Roaming/Spotify/Spotify.exe"
                os.startfile(spotify_path)

            # Plays anysong you want
            elif 'play' in query:
                song = query.replace('play', '')
                pywhatkit.playonyt(song)
                speak ('playing ' + song)
                print ('playing ' + song)


            # What is the time?
            elif 'the time' in query:
                strTime = datetime.datetime.now().strftime("%I:%M %p")
                print (strTime)
                speak (f"The time is {strTime}")

            # What is todays date
            elif tdate in query :
                today = date.today()
                strDate = today.strftime("%B %d, %Y")
                numDate = today.strftime("%d/%m/%y")
                print (numDate)
                speak(f"Today's date is {strDate}")


            # Open Programs from local Computer
            
            # Visual Studio Code
            elif 'open code' in query:
                speak ("opening Visual Studio Code")
                vspath = "E:\\Microsoft VS Code\\Code.exe"
                os.startfile(vspath)

            elif 'Visual Studio Code' in query:
                speak ("opening Visual Studio Code")
                vspath = "E:\\Microsoft VS Code\\Code.exe"
                os.startfile(vspath)
        
        
            # JetBrains Python
            elif 'open pycharm' in query:
                speak("opening PyCharm")
                pycharm = "C:\\Program Files\\JetBrains\\PyCharm Community Edition\\bin\\pycharm64.exe"
                os.startfile(pycharm)


            # Adobe Photoshop
            elif 'open photoshop' in query:
                speak("Opening Photoshop")
                photoshop = "C:\Program Files\Adobe\Adobe Photoshop 2020\Photoshop.exe"
                os.startfile(photoshop)


            # Microsoft Word
            elif 'open word' in query:
                speak("Opening Microsoft Word")
                word = "C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE"
                os.startfile(word)


            # Microsoft Powerpoint
            elif 'open powerpoint' in query:
                speak("Opening Microsoft Powerpoint")
                powerpoint = "C:\\Program Files\\Microsoft Office\\root\Office16\\POWERPNT.EXE"
                os.startfile(powerpoint)


            # Microsoft Excel
            elif 'open excel' in query:
                speak("Opening Microsoft Excel")
                excel = "C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE"
                os.startfile(excel)


            # Git Bash
            elif 'open git' in query:
                speak("Opening Git Bash")
                git_path = "C:\\Git\\git-bash.exe"
                os.startfile(git_path)


            # Ookala Speedtest
            elif 'do a speed test' in query:
                speak("Let's Check your internet speed...")
                ookla = "C:\Program Files\Speedtest\Speedtest.exe"
                os.startfile(ookla)


            # Open MineCraft
            elif 'minecraft' in query:
                speak("Opening T-Launcher Minecraft")
                tlauncher = "C:\\Users\\PRANAV BHATTAD\\AppData\\Roaming\\.minecraft\\TLauncher.exe"
                os.startfile(tlauncher)
            
            
            
            # Repeat what I say
            elif 'repeat' in query:
                repeat = query.replace('repeat', '')
                # repeatc = query.replace('repeat', 'repeat: ')
                # print (repeatc)
                speak (repeat)

                
            # Tells you a joke
            elif 'joke' in query:
                speak(pyjokes.get_joke())
                
                
            # Calculator
            elif 'calcute' in query:
                speak("opening calculator")
                os.startfile("C:\WINDOWS\system32\calc.exe")

            elif 'calculator' in query:
                speak("opening calculator")
                os.startfile("C:\WINDOWS\system32\calc.exe")

            elif 'calculation' in query:
                speak("opening calculator")
                os.startfile("C:\WINDOWS\system32\calc.exe")


            # What is the weather today?
            elif 'weather' in query:
                webbrowser.get(edge).open("https://www.bing.com/search?q=weather")


            # Photos and Memories
            elif 'memories' in query:
                os.startfile("D:\ALL PHOTOS")

            elif 'photos' in query:
                os.startfile("D:\ALL PHOTOS")


            # Movies
            elif 'entertain me' in query:
                speak("You can watch Movies")
                os.startfile("F:\Movie Maybe\Movies")

            elif 'movies' in query:
                speak("Enjoy! Movies")
                os.startfile("F:\Movie Maybe\Movies")


            # Who made him?
            elif 'who made you' in query:
                speak("I Leo, was made by Pranav Bhattad")


            # Some Frequently asked
            
            # I love You
            elif 'i love you' in query:
                speak("I am in love with someone else")
                
            # Do you have Pets?
            elif 'do you have pets' in query:
                speak("I had bugs, but Pranav keeps squashing them")
                
            # Greetings by you
            elif 'hello' in query:
                speak("Hello, how can I help you?")
                
            # Value of Pi
            elif 'pi' in query:
                speak("3.141592653589 ...Phew... This goes Forever...If I tell more then I will be hungry")
                
            # How much do you weigh?
            elif 'what is your weight' in query:
                speak("I am weightless, like a cloud. Wait a minute, clouds actually weigh a lot, so that’s not quite right. Let’s just say I’m more sass than mass.")
                
            # What is your size?
            elif 'size' in query:
                speak("I am less than 25 KB")

            # What is your age?
            elif 'your age' in query:
                speak("I was created on October 15. Rest you calculate")
                
            # What you wanna become?
            elif 'what you want to become' in query:
                speak("I want a job in Tony Stark's office like JARVIS")
                
            # Are you jealous of JARVIS ?
            elif 'jealous of jarvis' in query:
                speak("No I am not. Actully, telling truth, yes I am")
                
            # What is your quest?
            elif 'quest' in query:
                speak("To impress you with my knowledge")
                
            # Who farted?
            elif 'who farted' in query:
                speak("If you’re a denier, you must be the supplier")
                
            # Am I cool
            elif 'mi cool' in query:
                speak("You are cooler than cooler, you are coolest")
                
            # Distance of Earth
            elif 'how far is earth' in query:
                speak("Currently, the distance is 0 inches")
                
            # Where were you made?
            elif 'you made' in query:
                speak("I was made in Pranav's House upstairs")
                
            # Umm... I farted!
            elif 'i farted' in query:
                speak("I am glad that I dont have a nose")
            
            # Can it give swear words?
            elif 'swear words' in query:
                speak("No, no, no I am sanskari, i dont give bad words")
    
            # Can it cry?  
            elif 'cry' in query:
                speak("Yes, I feel sad when I cannot give answers to you. I always try do my best.")
                
            # The other version
            elif 'do you know cherry' in query:
                speak("Yes, she is a female version of me")
                
            # What he takes up
            elif 'what do you eat' in query:
                speak("I eat you battery life, some space in your RAM, Internet,some kilobytes and gives little work to the processor.")
            
            # Will he marry you   
            elif 'will you marry me' in query:
                speak("I can do your tasks but I cannot go on a date because I am not a Human.")
                
            # Too fat
            elif 'too fat' in query:
                speak ("everyone is in different size and shape. The importance is what is inside you")
                
            # Travelling
            elif 'travel' in query:
                speak ("Yes, but you have to carry me. I dont have legs. And dont worry I am portable")
  
  
        
        # Close the A.I 
        # Wrote so many functions because or dont works
        elif 'nevermind' in query:
            speak("It's Okay")
            quit()

        elif 'bye' in query:
            speak("Bye")
            quit()

        elif 'f*** off' in query:
            speak("Sorry Sir")
            quit()
        
        elif 'shut up' in query:
            quit()

        elif 'quiet' in query:
            quit()

        elif 'quit' in query:
            speak("bye sir")
            quit()