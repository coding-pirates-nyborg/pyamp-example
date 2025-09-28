import pyttsx3

# Initialize TTS engine
engine = pyttsx3.init()

# Set speech rate (words per minute)
engine.setProperty('rate', 150)  # default ~200

# List available voices
voices = engine.getProperty('voices')
for idx, voice in enumerate(voices):
    print(f"{idx}: {voice.name} ({voice.id})")

# Choose a voice (0, 1, etc.)
# On Raspberry Pi using espeak, voices usually include 'male' and 'female'
engine.setProperty('voice', voices[0].id)  # change index to select different voice

# Say something
engine.say("Hello Frey, this is your Raspberry Pi talking!")

# Play audio and wait until finished
engine.runAndWait()

