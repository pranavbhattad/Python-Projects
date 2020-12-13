# importing modules
import pyttsx3
import datetime
from datetime import date
from requests import get
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import speech_recognition as sr
import wikipedia
import time
import os
import webbrowser
import pywhatkit
import pyjokes
import ctypes
import random
import sys
import wolframalpha
import pyautogui
import requests
import tkinter as tk


#  voice or speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
client = wolframalpha.Client('9QLRHU-A28J3VK98X')

# what is speak? defining it...
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# Root Tkinter
root = tk.Tk()
root.withdraw()

#  Web Browser (Windows)
chrome = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
edge = 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe %s'
tdate = "what is today's date"
ttdate = "what is today's date"


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
    print("I am Leo. Please tell how may I help you?")


# Fuction New (Tells the new headlines)
def news():
    news_links = ['http://newsapi.org/v2/top-headlines?sources=techcrunch&apiKey=bbbd50febd70401080058f343bb3a44a', 'http://newsapi.org/v2/everything?q=bitcoin&from=2020-11-11&sortBy=publishedAt&apiKey=bbbd50febd70401080058f343bb3a44a', 'http://newsapi.org/v2/top-headlines?country=us&category=business&apiKey=bbbd50febd70401080058f343bb3a44a', 'http://newsapi.org/v2/top-headlines?country=in&category=business&apiKey=bbbd50febd70401080058f343bb3a44a', 'http://newsapi.org/v2/everything?q=apple&from=2020-12-10&to=2020-12-10&sortBy=popularity&apiKey=bbbd50febd70401080058f343bb3a44a', 
'http://newsapi.org/v2/everything?domains=wsj.com&apiKey=bbbd50febd70401080058f343bb3a44a']
    
    main_url = random.choice(news_links)
    main_page = get(main_url).json()
    articles = main_page["articles"]
    head = []
    day = ["First", "Second", "Third", "Four", "Five"]
    for ar in articles:
        head.append(ar["title"])
    for i in range (len(day)):
        speak(f"today's {day[i]} news is {head[i]}")
        
        
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

    except sr.UnknownValueError:
        speak('Sorry sir! I didn\'t get that! Try typing the command!')
        query = str(input('>>> '))
        
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
            

            # IP Address
            elif 'ip address' in query or 'what is my ip address' in query:
                ip = get('https://api.ipify.org').text
                print(f"Your IP address is: {ip}")
                speak(f"your IP address is {ip}")
            
            
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


            # Instagram
            elif 'open instagram' in query or 'instagram' in query:
                speak("Opening your Instagram Handle")
                webbrowser.get(chrome).open("instagram.com")
             
                
            # Facebook
            elif 'facebook' in query:
                speak("Opening Facebook")
                webbrowser.get(chrome).open("facebook.com")
                
                
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
            
            
            #  Open and Close Spotify
            elif 'spotify' in query:
                speak ("Opening Spotify... Enjoy Music")
                spotify_path = "C:/Users/PRANAV BHATTAD/AppData/Roaming/Spotify/Spotify.exe"
                os.startfile(spotify_path)
                
            elif 'close spotify' in query:
                speak("Opening Spotify... Enjoy Music")
                os.system("taskkill /f /im Spotify.exe")

            # Plays any song you want
            elif 'play' in query:
                song = query.replace('leo play', '')
                pywhatkit.playonyt(song)
                speak ('playing ' + song)
                print ('playing ' + song)


            # What is the time?
            elif 'what is the time' in query:
                strTime = datetime.datetime.now().strftime("%I:%M %p")
                print (strTime)
                speak (f"The time is {strTime}")

            # What is todays date
            elif tdate in query or ttdate in query:
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

            elif 'open Visual Studio Code' in query:
                speak ("opening Visual Studio Code")
                vspath = "E:\\Microsoft VS Code\\Code.exe"
                os.startfile(vspath)
        
        
            # JetBrains Python
            elif 'open pycharm' in query:
                speak("opening PyCharm")
                pycharm = "C:\\Program Files\\JetBrains\\PyCharm Community Edition\\bin\\pycharm64.exe"
                os.startfile(pycharm)


            # Whatsapp 
            elif 'open whatsapp' in query:
                speak("opening whatsapp")
                wdir = "C:\\Users\\PRANAV BHATTAD\\AppData\\Local\\WhatsApp\\WhatsApp.exe"
                os.startfile(wdir)

            # Notepad
            elif 'open notepad' in query:
                speak("opening Notepad")
                npath = "C:\\Windows\\System32\\notepad.exe"
                os.startfile(npath)


            # Command Promp
            elif 'open cmd' in query:
                speak("Opening Command Prompt")
                os.system("start cmd")

            elif 'open command prompt' in query:
                speak("Opening Command Prompt")
                
                
            # Adobe Photoshop
            elif 'open photoshop' in query:
                speak("Opening Adobe Photoshop")
                photoshop = "C:\Program Files\Adobe\Adobe Photoshop 2020\Photoshop.exe"
                os.startfile(photoshop)


            # Camera
            elif 'open camera' in query:
                speak("switching to camera please smail")
                os.system('start microsoft.windows.camera:')
                
                
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
            elif 'open git' in query or 'open get' in query:
                speak("Opening Git Bash")
                git_path = "C:\\Git\\git-bash.exe"
                os.startfile(git_path)


            # Ookala Speedtest
            elif 'do a speed test' in query:
                speak("Let's Check your internet speed...")
                ookla = "C:\Program Files\Speedtest\Speedtest.exe"
                os.startfile(ookla)


            # Open MineCraft
            elif 'open minecraft' in query:
                speak("Opening T-Launcher Minecraft")
                tlauncher = "C:\\Users\\PRANAV BHATTAD\\AppData\\Roaming\\.minecraft\\TLauncher.exe"
                os.startfile(tlauncher)
            
            
            # Close programs from local computer
            
            # Visual Studio Code
            elif 'close code' in query:
                speak ("closing Visual Studio Code")
                os.system("taskkill /f /im Code.exe")

            elif 'close visual studio code' in query:
                speak ("closing Visual Studio Code")
                os.system("taskkill /f /im Code.exe")
                
                
            # JetBrains Python
            elif 'close pycharm' in query:
                speak("closing PyCharm")
                os.system("taskkill /f /im pycharm64.exe")
                
                
            # Notepad
            elif 'close notepad' in query:
                speak("closing Notepad")
                os.system("taskkill /f /im notepad.exe")


            # Command Promp
            elif 'close cmd' in query:
                speak("Closing Command Prompt")
                os.system("taskkill /f /im cmd.exe")

            elif 'close command prompt' in query:
                speak("Closing Command Prompt")
                os.system("taskkill /f /im cmd.exe")
                
                
            # Adobe Photoshop
            elif 'close photoshop' in query:
                speak("closing Adobe Photoshop")
                os.system("taskkill /f /im Photoshop.exe")


            # Camera
            elif 'close camera' in query:
                speak("Closing camera")
                os.system('taskkill /f /im WindowsCamera.exe')


            # Microsoft Word
            elif 'close word' in query:
                speak("Closing Microsoft Word")
                os.system('taskkill /f /im WindowsCamera.exe')


            # Microsoft Powerpoint
            elif 'close powerpoint' in query:
                speak("Closing Microsoft Powerpoint")
                os.system('taskkill /f /im POWERPNT.EXE')


            # Microsoft Excel
            elif 'close excel' in query:
                speak("Closing Microsoft Excel")
                os.system('taskkill /f /im EXCEL.EXE')


            # Git Bash
            elif 'close git' in query or 'close get' in query:
                speak("Closing Git Commant Line")
                os.system('taskkill /f /im git-bash.exe')


            # Ookala Speedtest
            elif 'close speed test' in query:
                speak("Closing ookala Speedtest")
                os.system('taskkill /f /im Speedtest.exe')
                
                
            # Open MineCraft
            elif 'close minecraft' in query:
                speak("Closing T-Launcher Minecraft")
                os.system('taskill /f /im TLauncher.exe')
                
                
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

            # Hide the folder
            elif 'hide the folder' in query or 'hide a folder' in query:
                speak("Are you sure?")
                condition = takeCommand().lower()
                
                if 'hide' in condition or 'sure' in condition or 'yes' in condition:
                    speak("Please select a folder, if you can't see the window then got to your desktop")
                    fdir = filedialog.askdirectory()
                    ffdir = '"'+fdir+'"'
                    command = 'attrib +s +h /d '+ ffdir
                    os.system(command)
                    speak("The folder is hidden, To unhide it see the Unhide.txt file")
                    
                elif 'no' in condition or 'abort' in condition or 'leave' in condition:
                    speak("Mission Hiding Folders Aborted")


            # What is today's news?
            elif 'news' in query:
                speak("Please wait fetching the latest news")
                news()
                
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


            # What is my location?
            elif 'where i am' in query or 'location' in query:
                speak("Tracking you location")
                try:
                    ipAdd = requests.get('https://api.ipify.org').text
                    url = 'https://get.geojs.io/v1/ip/geo/'+ipAdd+'.json'
                    geo_requests = requests.get(url)
                    geo_data = geo_requests.json()
                    
                    city = geo_data['city']
                    state = geo_data['region']
                    country = geo_data['country']
                
                    print(f"Sir according to records, you are in Ichalkaranji city, {state},  {country}.")
                    speak(f"Sir according to records, you are in Ichalkaranji city, {state}, {country}.")
                    
                except Exception as e:
                    speak("Due to some error we couldn't find the location")
                    pass
                
                
                
            # Some Frequently asked
            
            # I love You
            elif 'i love you' in query:
                say = ['I am in love with wifi', 'I am a assistant', 'I can tell you the dtae, cant be your date']
                speak(random.choice(say))
                
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
                speak("I am currently in KB's")

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
  
  
                # Making changes to computer. (Only for WINDOWS)
        elif 'shut down the system' in query:
            os.system("shutdown /s /t 5")
        
        elif 'restart the system' in query:
            os.system("shutdown /r /t 5")
        
        elif 'sleep the system' in query:
            ctypes.windll.user32.LockWorkStation()
        
        elif 'force sleep the system' in query:
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
          
          
            
        # Repeat what I say
        elif 'repeat' in query:
            repeat = query.replace('repeat', '')
            # repeatc = query.replace('repeat', 'repeat: ')
            # print (repeatc)
            speak (repeat) 
            
            
        # Takes a screenshoT
        elif 'take screenshot' in query or 'take a screenshot' in query:
            speak("Please input me a Name for this screenshot")
            name = input("Enter the file name:")
            speak("Please hold the screen. You are getting two seconds to do it. I am taking the screenshot")
            time.sleep(3)
            img = pyautogui.screenshot()
            img.save(f"{name}.png")
            speak("The screenshot is saved in this directory")
            
        
        # Switch the windows
        elif 'switch to window' in query:
            pyautogui.keyDown("alt")
            pyautogui.press("tab")
            time.sleep(0.5) 
            pyautogui.keyUp("alt")
            
            
        # Close the A.I 
        # Wrote so many functions peoplencan say anything
        elif 'nevermind' in query:
            speak("It's Okay")
            quit()

        elif 'bye' in query:
            speak("Bye")
            quit()

        elif 'f*** off' in query:
            speak("Sorry Sir")
            quit()

        elif 'deactivate' in query or 'abort' in query:
            quit()

        elif 'quiet' in query or 'shut up' in query:
            quit()

        elif 'quit' in query:
            speak("bye sir")
            quit()

            
        # All the what is question (Putting in last to ac=void errors)
        elif 'what is' in query or 'what are' in query:
            try:
                if f'what is {query}' :
                    query = query.replace('what is', '')
                    query = query.replace('what are', '')
                    res = client.query(query)
                    results = next(res.results).text
                    speak("fetching results...")
                    print(results)
                    speak(results)
                    
            except StopIteration:
                print("No Results!")
                speak("No Results!")
                
            except AttributeError:
                speak("Can you repeat again?")
                
            except Exception:
                speak("Can you say it more clearly?")