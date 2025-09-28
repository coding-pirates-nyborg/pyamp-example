from gtts import gTTS
#tts = gTTS("Jespers mom is SO fat that....", lang="en")

# Australian English (again, different voice/accent)
tts = gTTS("Hello Frey, this is Australian English.", lang="en", tld="com.au")
tts.save("fat_mom.mp3")

