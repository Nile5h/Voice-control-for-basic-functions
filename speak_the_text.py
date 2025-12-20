import pyttsx3

en = pyttsx3.init()
en.setProperty('voice', en.getProperty('voices')[1].id)
en.say("suzume")
en.runAndWait()

voices = en.getProperty('voices')
for voice in voices:
        print(f"ID: {voice.id}, Name: {voice.name}, Gender: {voice.gender}")
en.setProperty('voice', voices[0].id)

en.say("Hello, I am using a different voice now.")
en.runAndWait()