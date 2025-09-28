#!/usr/bin/env python3
"""
Working TTS solution that pipes espeak through aplay to use the correct audio device.
This bypasses espeak's audio configuration issues.
"""

import subprocess
import sys
import os

class WorkingTTS:
    def __init__(self, rate=150, volume=80):
        self.rate = rate
        self.volume = volume
        
    def say(self, text):
        """Speak text using espeak piped through aplay"""
        try:
            # Create espeak command
            espeak_cmd = [
                "espeak", 
                text, 
                "--stdout",
                "-s", str(self.rate),  # speed
                "-a", str(self.volume)  # amplitude (0-200)
            ]
            
            # Create aplay command to use our configured default device
            aplay_cmd = ["aplay", "-D", "default"]
            
            # Create the pipeline
            espeak_process = subprocess.Popen(espeak_cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
            aplay_process = subprocess.Popen(aplay_cmd, stdin=espeak_process.stdout, stderr=subprocess.DEVNULL)
            
            # Wait for completion
            espeak_process.stdout.close()
            aplay_process.communicate()
            
        except Exception as e:
            print(f"TTS Error: {e}")
    
    def set_rate(self, rate):
        """Set speech rate (words per minute)"""
        self.rate = rate
        
    def set_volume(self, volume):
        """Set volume (0.0 to 1.0)"""
        self.volume = int(volume * 100)

def main():
    # Test the working TTS
    tts = WorkingTTS()
    
    print("Testing working TTS solution...")
    tts.say("Hello! This is a working text to speech solution that uses your MAX98357A correctly!")
    
    print("Testing different rates...")
    tts.set_rate(100)
    tts.say("This is slow speech")
    
    tts.set_rate(200)
    tts.say("This is fast speech")
    
    tts.set_rate(150)
    tts.say("This is normal speed")
    
    print("TTS test complete!")

if __name__ == "__main__":
    main()
