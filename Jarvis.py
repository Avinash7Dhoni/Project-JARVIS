import speech_recognition as sr
import pyttsx3
import pywhatkit
import wikipedia
from datetime import datetime as dt,timedelta
import sys
import time
import threading
# Initialize recognizer and TTS engine
r=sr.Recognizer()
speaker=pyttsx3.init()
rate = speaker.getProperty('rate')   # getting details of current speaking rate                  
speaker.setProperty('rate', 200)     # setting up new voice rate
voices =speaker.getProperty('voices')       #getting details of current voice
#engine.setProperty('voice', voices[0].id)  #changing index, changes voices. o for male
speaker.setProperty('voice', voices[1].id)   #changing index, changes voices. 1 for female
mic_list=sr.Microphone.list_microphone_names()
Assistant="JARVIS"
#Defining reminders
reminders=[]
#speak_lock is a threading lock used to ensure that speak function is not called concurrently by multiple threads
speak_lock=threading.Lock()
def speak(text):
    with speak_lock:
        speaker.say(text)
        speaker.runAndWait()
def take_command():
    command=''
    with sr.Microphone() as source:
        try:
            print("LISTENING...")
            speak("Is there anything else i can do for you?")

            voice=r.listen(source,timeout=5,phrase_time_limit=10)
            command=r.recognize_google(voice).upper()
            #command=command.upper()
            if Assistant in command:
                command=command.replace(Assistant+' ','')
                print("command recievied:",command)
                #speak(command)
        except sr.WaitTimeoutError:
                print("Listening timed out. Please try again.")
                speak("Listening timed out. Please try again.")
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand the audio.")
            speak("Google Speech Recognition could not understand the audio.")
        except Exception as e:
                print("Check your microphone") 
                speak("Check your microphone") 
    return command 
def set_alarm(alarm_time):
    def alarm_thread():
        while True:
            current_time = dt.now().strftime("%H:%M")
            if current_time == alarm_time:
                print("Wake up! It's time!")
                speak("Wake up! It's time!")
                break
            time.sleep(10)  
    threading.Thread(target=alarm_thread).start() 
def set_reminder(reminder_time, reminder_message):
    reminders.append((reminder_time, reminder_message))
    
    def reminder_thread():
        while True:
            current_time = dt.now().strftime("%H:%M")
            for reminder in reminders:
                if current_time == reminder[0]:
                    print(f"Reminder: {reminder[1]}")
                    speak(f"Reminder: {reminder[1]}")
                    reminders.remove(reminder)
                    break
            time.sleep(10)
    threading.Thread(target=reminder_thread).start() 
def process_command(command):
    if 'HELLO' in command :
        greet_user()

    elif 'TIME' in command:
        A=dt.now().strftime("%H:%M:%S")
        print("current time is"+A)
        speak("Current time is"+A)
    elif 'DATE'in command:
        B=dt.now().strftime("%Y-%m-%d")
        print("present date is:"+B)
        speak("Present date is:"+B)
    elif 'SEARCH' in command or 'BROWSE' in command:
        command=command.replace('SEARCH','')
        print("Browsing for"+command+"GO ON SIR")
        speak(command)
        pywhatkit.search(command)  
        return False
    elif ' SET ALARM FOR' in command:
        alarm_time = command.replace('SET ALARM FOR ', '').strip()
        print("Setting alarm for " + alarm_time)
        speak("Setting alarm for " + alarm_time)
        set_alarm(alarm_time)
    elif 'SET REMINDER FOR' in command:
        try:
            parts = command.replace('SET REMINDER FOR ', '').split(' TO ')
            reminder_time = parts[0].strip()
            reminder_message = parts[1].strip()
            print(f"Setting reminder for {reminder_time} to {reminder_message}")
            speak(f"Setting reminder for {reminder_time} to {reminder_message}")
            set_reminder(reminder_time, reminder_message)
        except IndexError:
            speak("I didn't catch that. Please say the reminder in the format 'set reminder for [time] to [message]'")
    elif 'WHAT' in command or 'WHO' in command:
        command=command.replace('who','')
        info=wikipedia.summary(command,2)
        print(info)
        speak(info)
        return False
    elif 'PLAY' in command:
        command=command.replace('PLAY','')
        print("playing"+command)
        speak("playing"+command+"Enjoy Boss")
        pywhatkit.playonyt(command)
        return False
    elif 'SEARCH' in command or 'TELL ME' in command:
        command=command.replace('TELL ME',"")
        print("hmm")
        pywhatkit.search(command)
        speak (command)
        return False 
    elif "EXIT" in command or "BYE" in command:
        print("Signing off")
        speak("Signing off")  
        return False
    else:
        speak("I'm sorry,i didn't understand Please try again") 
    return True 
def greet_user():
    current_hour=dt.now().hour
    if 0<= current_hour<12:
        greet="GOOD MORNING!"
    elif 12<=current_hour<17:
        greet="GOOD AFTERNOON"
    elif 17<=current_hour<21:
        greet="GOOD EVENING"
    else:
        greet="GOOD NIGHT"
    print(greet)
    speak(greet)
def listen():
    while True:
        command=take_command()
        if command:
            if not process_command(command):
                break
print("Welcome sir!")
speak("Welcome sir!")
listen() 