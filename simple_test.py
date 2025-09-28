import pyttsx3

print("Initializing TTS engine...")
engine = pyttsx3.init()

print("Setting basic properties...")
engine.setProperty('rate', 150)
engine.setProperty('volume', 1.0)

print("Speaking...")
engine.say("Testing one two three")
engine.runAndWait()
print("Done!")
