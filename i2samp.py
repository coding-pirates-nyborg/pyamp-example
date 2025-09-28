import os

try:
    from adafruit_python_shell import shell
    from clint.textui import colored
except ImportError:
    raise RuntimeError("The library 'adafruit-python-shell' was not found. To install, try typing: sudo pip3 install adafruit-python-shell")

# Create shell instance for backwards compatibility
Shell = shell_instance.Shell
shell_instance = Shell()

BLACKLIST = "/etc/modprobe.d/raspi-blacklist.conf"
PRODUCT_NAME = "I2S Amplifier"
OVERLAY = "googlevoicehat-soundcard"

def driver_loaded(driver_name):
    return shell_instance.run_command(f"lsmod | grep -q '{driver_name}'", suppress_message=True)

def main():
    reboot = False
    shell_instance.clear()
    if not shell_instance.is_raspberry_pi():
        shell_instance.bail("Non-Raspberry Pi board detected.")
    print("\nThis script will install everything needed to use\n"
        f"{PRODUCT_NAME}.\n")
    print(colored.red("--- Warning ---"))
    print("\nAlways be careful when running scripts and commands\n"
        "copied from the internet. Ensure they are from a\n"
        "trusted source.\n")
    if not shell_instance.prompt("Do you wish to continue?"):
        print("\nAborting...")
        shell_instance.exit()

    print("\nChecking hardware requirements...")

    # Enable I2S overlay
    config = shell_instance.get_boot_config()
    if config is None:
        shell_instance.bail("No Device Tree Detected, not supported")

    print(f"\nAdding Device Tree Entry to {config}")

    if shell_instance.pattern_search(config, f"^dtoverlay={OVERLAY}$"):
        print("dtoverlay already active")
    else:
        shell_instance.write_text_file(config, f"dtoverlay={OVERLAY}")
        reboot = True

    if os.path.exists(BLACKLIST):
        print("\nCommenting out Blacklist entry in", BLACKLIST)
        shell_instance.pattern_replace(BLACKLIST, "^blacklist[[:space:]]*snd_soc_max98357a.*", "#blacklist snd_soc_max98357a")
        shell_instance.pattern_replace(BLACKLIST, "^blacklist[[:space:]]*snd_soc_max98357a_i2c.*", "#blacklist snd_soc_max98357a_i2c")
        shell_instance.pattern_replace(BLACKLIST, "^blacklist[[:space:]]*snd_soc_max98357a.*", "#blacklist snd_soc_max98357a")

    print("Configuring sound output")
    if os.path.exists("/etc/asound.conf"):
        if os.path.exists("/etc/asound.conf.old"):
            shell_instance.remove("/etc/asound.conf.old")
        shell_instance.move("/etc/asound.conf", "/etc/asound.conf.old")
    shell_instance.write_text_file("~/asound.conf",
"""
pcm.speakerbonnet {
   type hw card 0
}

pcm.dmixer {
   type dmix
   ipc_key 1024
   ipc_perm 0666
   slave {
     pcm "speakerbonnet"
     period_time 0
     period_size 1024
     buffer_size 8192
     rate 44100
     channels 2
   }
}

ctl.dmixer {
    type hw card 0
}

pcm.softvol {
    type softvol
    slave.pcm "dmixer"
    control.name "PCM"
    control.card 0
}

ctl.softvol {
    type hw card 0
}

pcm.!default {
    type             plug
    slave.pcm       "softvol"
}
""")
    shell_instance.move("~/asound.conf", "/etc/asound.conf")


    print("Installing aplay systemd unit")
    shell_instance.write_text_file("/etc/systemd/system/aplay.service", """
[Unit]
Description=Invoke aplay from /dev/zero at system start.

[Service]
ExecStart=/usr/bin/aplay -D default -t raw -r 44100 -c 2 -f S16_LE /dev/zero

[Install]
WantedBy=multi-user.target""", append=False)

    shell_instance.run_command("sudo systemctl daemon-reload")
    shell_instance.run_command("sudo systemctl disable aplay")
    print("\nYou can optionally activate '/dev/zero' playback in\n"
        "the background at boot. This will remove all\n"
        "popping/clicking but does use some processor time.\n\n")
    if shell_instance.prompt("Activate '/dev/zero' playback in background? [RECOMMENDED]\n", default="y"):
        shell_instance.run_command("sudo systemctl enable aplay")
        reboot = True

    if driver_loaded("max98357a"):
        print(f"\nWe can now test your {PRODUCT_NAME}")
        shell_instance.warn("Set your speakers at a low volume if possible!")
        if shell_instance.prompt("Do you wish to test your system now?"):
            print("Testing...")
            shell_instance.run_command("speaker-test -l5 -c2 -t wav")
    print("\n" + colored.green("All done!"))
    print("\nEnjoy your new $productname!")
    if reboot:
        shell_instance.prompt_reboot()

# Main function
if __name__ == "__main__":
    shell_instance.require_root()
    main()
