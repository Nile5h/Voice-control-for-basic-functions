import speech_recognition as sr
import webbrowser
import pyttsx3
import datetime ,open_library
import music_library as music
import threading
import subprocess
import google.generativeai as genai
import os
import yt_dlp, wikipedia, conv_save
# import opencv


API_KEY = ""
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel(
    "gemini-2.0-flash",
    generation_config={
        "temperature": 0.3,       # lower = less creative, more precise
        "max_output_tokens": 100,  # limit answer length
        "top_p": 0.8,
        "top_k": 40,
    }
)

recognizer = sr.Recognizer()
Music_folder='C:\\Users\\ok\\Documents\\Jarvis\\music'

def time():
    now = datetime.datetime.now()
    return now.strftime("%H hour %M minutes and %S seconds")

def download_song(song):
    try:
            query = f"ytsearch1:{song}"
            with yt_dlp.YoutubeDL({'format': 'bestaudio'}) as ydl:
                info = ydl.extract_info(query, download=False)['entries'][0]
                title = info['title']
            ydl_opts = {
                'outtmpl': os.path.join(Music_folder, f'{title}.mp3'),
                'format': 'bestaudio/best',
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([f'ytsearch:{song}'])
            
            music.add(song, title)  # Add to music library
            song_path = os.path.join(Music_folder,f"{title}.mp3")
            os.startfile(song_path)
            speak(f"{song} Downloaded locally", c)
            return title
    except Exception as e:
            speak(f"Error downloading {song}: {e}", c)

def play_youtube(song):
    query = f"ytsearch1:{song}"  # search YouTube and get 1 result
    with yt_dlp.YoutubeDL({'format': 'bestaudio'}) as ydl:
        info = ydl.extract_info(query, download=False)['entries'][0]
        url = f"https://www.youtube.com/watch?v={info['id']}"
        webbrowser.open(url)
    speak(f"Playing {info['title']} on YouTube",c)

def play_localy(song):
    div = music.get(song)
    if div :
        titl = div
        try:
            song_pa = os.path.join(Music_folder,f"{titl}.mp3")
            os.startfile(song_pa)
            speak(f"Playing {titl} locally", c)
        except Exception as e:
            speak(f"Error playing {song}: {e}", c)
    else:
        speak(f"{song} not found locally. Downloading...", c)
        title = download_song(song)
        song_path = os.path.join(Music_folder,f"{title}.mp3")
        os.startfile(song_path)
        speak(f"Playing {song} locally", c)

def speak(text, req):
    def run():
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    threading.Thread(target=run).start()
    print("Google:", text)
    conv_save.save_conversation(req, text, time())


def processCommand(c):
    if "open" in c.lower():
        app= c.lower().split()[1]
        link = open_library.open[app]
        webbrowser.open(link)
        speak(f"opening {app}", c)

    elif "current time" in c.lower():
        speak(time(),c)

    elif c.lower().startswith("play"):
        if "localy" in c.lower() or "from laptop" in c.lower():
            song = c.replace("play", "").replace("localy", "").strip()
            play_localy(song)
        elif "youtube" in c.lower():
            song = c.replace("play", "").strip()
            play_youtube(song)
        else:
            song = c.replace("play", "").strip()
            play_youtube(song)

    elif "news" in c.lower():
        webbrowser.open("https://news.google.com")
        speak("Here are some news from google news",c)

    elif "download" in c.lower():
        song = c.replace("download", "").strip()
        download_song(song)

    elif "calculate" in c.lower():
        equation = c.replace("calculate", "").strip()
        try:
            from Calculater import cal
            result = cal(equation)
            speak(f"The result is {result}",c)
        except Exception as e:
            speak(f"Error in calculation: {e}",c)

    # elif "information" in c.lower() or "give me info about" in c.lower() or "want to know about" in c.lower():
    #     try :
    #         search_results_list = wikipedia.search(c.lower()[])
    #         if search_results_list:
    #             first_title = search_results_list[0]
    #             summary_text = wikipedia.summary(first_title, sentences=4) # Assuming 'sen' variable defines number of sentences
    #             speak(summary_text, c)
    #         else:
    #             speak(f"Sorry, I couldn't find any Wikipedia results for {c}", c)

    #     except Exception as e:
    #         print(f"An error occurred: {e}")

    elif c.lower().startswith("write"):
        print(c[5:])
            
    else:        
        print("Directed to google.")
        respons = chat.send_message(c)
        speak(respons.text,c)
        

if __name__ == "__main__":
    speak("Initializing Google...", "Start")
    # gemini chat initlizing
    chat = model.start_chat()
    var = True
    while var:
    # listen for the wake word "hey google"
    # obtain audio from the microphone
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=1)
                print("Listening for wake word.....")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=2)
            print("Recognizing....")
            word = recognizer.recognize_google(audio)
            print("you :",word)
            # word = input("Input: ")
            
            if "hey google" in word.lower():
                # listen for command

                with sr.Microphone() as source:
                    recognizer.adjust_for_ambient_noise(source, duration=1)  # longer calibration
                    print("Google Active.....")
                    speak("yeh, i am listening", word)
                    audio = recognizer.listen(source,timeout=5 , phrase_time_limit=4)
                    c = recognizer.recognize_google(audio)
                    # c=input("Input: ")
                processCommand(c)

            elif("stop it" in word.lower()):
                speak("Google Stopped..",word)
                var = False
    
        except sr.WaitTimeoutError:
            print("Timeout: No speech detected")
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print(f"API error: {e}")
        except Exception as e:
            print("General Error:", e)

    
    # print("Engine cleanly")


