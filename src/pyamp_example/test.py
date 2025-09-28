import pyttsx3

engine = pyttsx3.init()

voices = engine.getProperty('voices')

# Choose the voice you want by index
engine.setProperty('voice', voices[28].id)  # US English
# or
# engine.setProperty('voice', voices[23].id)  # UK English

engine.setProperty('rate', 150)    # Words per minute (default ~200)
engine.setProperty('volume', 0.8)  # 0.0 to 1.0


engine.say("Hello Frey, this is your Raspberry Pi speaking in the chosen voice!")
engine.runAndWait()


