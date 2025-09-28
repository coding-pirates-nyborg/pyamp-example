# MAX98357A I2S DAC Setup Guide

This guide will help you set up a Raspberry Pi with the MAX98357A I2S DAC for audio output and text-to-speech functionality.

## Hardware Requirements

- Raspberry Pi (any model with GPIO pins)
- MAX98357A I2S DAC breakout board
- Speaker (4-8 ohm, 3W max)
- Jumper wires

## Hardware Connections

Connect the MAX98357A to your Raspberry Pi GPIO pins:

| MAX98357A Pin | Raspberry Pi Pin | GPIO Pin |
|---------------|------------------|----------|
| VIN           | 5V (Pin 2)       | 5V       |
| GND           | GND (Pin 6)      | GND      |
| DIN           | Pin 40           | GPIO 21  |
| BCLK          | Pin 12           | GPIO 18  |
| LRC           | Pin 35           | GPIO 19  |

Optional connections:
- SD (Shutdown): Can be left unconnected (internal pull-up keeps it active)
- GAIN: Connect to GND for 9dB gain, VIN for 15dB gain, or leave floating for 12dB gain

## Software Setup

### 1. Enable I2S in Raspberry Pi Configuration

Edit the boot configuration:
```bash
sudo nano /boot/firmware/config.txt
```

Add this line to enable I2S:
```
dtparam=i2s=on
```

Reboot to apply changes:
```bash
sudo reboot
```

### 2. Install System Dependencies

Update your system and install required packages:
```bash
sudo apt update
sudo apt install -y espeak espeak-data alsa-utils
```

### 3. Configure ALSA for MAX98357A

Create the ALSA configuration file:
```bash
sudo nano /etc/asound.conf
```

Add this configuration:
```
pcm.!default {
    type plug
    slave.pcm "dmixer"
}

ctl.!default {
    type hw
    card 1
}

pcm.dmixer {
    type dmix
    ipc_key 1024
    ipc_perm 0666
    slave {
        pcm "hw:1,0"
        period_time 0
        period_size 1024
        buffer_size 4096
        rate 48000
        channels 2
    }
    bindings {
        0 0
        1 1
    }
}

pcm.speakerbonnet {
    type hw
    card 1
}

pcm.softvol {
    type softvol
    slave.pcm "dmixer"
    control.name "PCM"
    control.card 1
}

ctl.softvol {
    type hw
    card 1
}
```

Save and exit, then reboot:
```bash
sudo reboot
```

### 4. Verify Audio Setup

After reboot, check that your MAX98357A is detected:
```bash
aplay -l
```

You should see something like:
```
card 1: MAX98357A [MAX98357A], device 0: bcm2835-i2s-HiFi HiFi-0
```

Test audio output:
```bash
# Test with a system sound
aplay /usr/share/sounds/alsa/Front_Left.wav

# Test with speaker-test
speaker-test -D default -c2 -t sine -f 1000 -l 1
```

### 5. Set Up Python Environment

Install uv (modern Python package manager):
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc
```

Clone or create your project:
```bash
git clone <your-repo-url>
cd max98357a
```

Or create a new project with this `pyproject.toml`:
```toml
[project]
name = "pyamp-example"
version = "0.1.0"
description = "Small example that shows how to use the MAX98357A DAC"
readme = "README.md"
authors = [
    { name = "Your Name", email = "your.email@example.com" }
]
requires-python = ">=3.9"
dependencies = [
    "adafruit-python-shell",
    "clint",
    "pyttsx3"
]

[project.scripts]
pyamp-example = "pyamp_example:main"

[build-system]
requires = ["uv_build>=0.8.17,<0.9.0"]
build-backend = "uv_build"
```

Install Python dependencies:
```bash
uv sync
```

### 6. Test Text-to-Speech

Create a simple test script (`test_tts.py`):
```python
import pyttsx3

# Initialize the TTS engine
engine = pyttsx3.init()

# List available voices (optional)
voices = engine.getProperty('voices')
print(f"Available voices: {len(voices)}")

# Configure voice and speech properties
engine.setProperty('voice', voices[28].id)  # English (America)
engine.setProperty('rate', 150)    # Words per minute
engine.setProperty('volume', 0.8)  # Volume (0.0 to 1.0)

# Speak some text
engine.say("Hello! Your MAX98357A audio setup is working perfectly!")
engine.runAndWait()
```

Run the test:
```bash
uv run python test_tts.py
```

## Troubleshooting

### No Sound Output

1. **Check audio device detection:**
   ```bash
   aplay -l | grep MAX98357A
   ```

2. **Check for blocking processes:**
   ```bash
   sudo fuser -v /dev/snd/*
   ```
   Kill any blocking processes if found:
   ```bash
   sudo kill <PID>
   ```

3. **Test direct hardware access:**
   ```bash
   speaker-test -D hw:1,0 -c2 -t sine -f 1000 -l 1
   ```

### TTS Not Working

1. **Verify espeak installation:**
   ```bash
   espeak "Hello test"
   ```

2. **Test espeak with piping:**
   ```bash
   espeak "Hello test" --stdout | aplay -D default
   ```

3. **Check available voices:**
   ```bash
   uv run python -c "import pyttsx3; engine = pyttsx3.init(); voices = engine.getProperty('voices'); print(f'Available voices: {len(voices)}')"
   ```

### Audio Quality Issues

1. **Adjust buffer sizes** in `/etc/asound.conf`:
   - Increase `buffer_size` for better quality (higher latency)
   - Decrease for lower latency (potential audio dropouts)

2. **Adjust sample rate** if needed:
   - Change `rate 48000` to `rate 44100` in the dmixer configuration

3. **Check hardware connections** - loose connections can cause audio issues

## Voice Selection

Your system has 131+ voices available. Common English voices:
- Voice 23: English (Great Britain)
- Voice 27: English (Received Pronunciation) 
- Voice 28: English (America)
- Voice 29: English (America, New York City)

To list all voices:
```bash
uv run python -c "import pyttsx3; engine = pyttsx3.init(); voices = engine.getProperty('voices'); [print(f'{i}: {v.name} ({v.id})') for i, v in enumerate(voices)]"
```

## Performance Tips

1. **Use the dmixer configuration** - allows multiple applications to use audio simultaneously
2. **Set appropriate buffer sizes** - balance between latency and stability  
3. **Consider CPU usage** - TTS can be CPU intensive on older Pi models
4. **Test after system updates** - audio configuration may need verification

## Configuration Persistence

The configuration is permanent and will survive:
- ✅ System reboots
- ✅ Most system updates
- ✅ Audio service restarts

May need reconfiguration after:
- Major OS upgrades
- Manual deletion of `/etc/asound.conf`
- Hardware changes

---

Your MAX98357A I2S DAC setup is now complete and ready for audio projects!
