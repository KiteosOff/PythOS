import os
import time
import sys
import hashlib
import winsound
import datetime
from colorama import Fore, Back, Style, init

init()

VERSION = "1.4.6SE"

BOOT_SOUND = "pythos_boot.wav"
FAIL_SOUND = "pythos_bootfailure.wav"

# ======================
# UTIL
# ======================

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def play(sound):
    if os.path.exists(sound):
        winsound.PlaySound(sound, winsound.SND_FILENAME)

def slow(text, speed=0.015):
    for c in text:
        print(c, end="", flush=True)
        time.sleep(speed)
    print()

# ======================
# ANNIVERSAIRE
# ======================

def is_birthday():

    today = datetime.datetime.now()

    # modifie ici la date
    return today.month == 5 and today.day == 5

# ======================
# LOGO
# ======================

def show_logo():

    logo = [
"██████╗ ██╗   ██╗████████╗██╗  ██╗ ██████╗ ███████╗",
"██╔══██╗╚██╗ ██╔╝╚══██╔══╝██║  ██║██╔═══██╗██╔════╝",
"██████╔╝ ╚████╔╝    ██║   ███████║██║   ██║███████╗",
"██╔═══╝   ╚██╔╝     ██║   ██╔══██║██║   ██║╚════██║",
"██║        ██║      ██║   ██║  ██║╚██████╔╝███████║",
"╚═╝        ╚═╝      ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚══════╝"
]

    color = Fore.YELLOW if is_birthday() else Fore.CYAN

    print()

    for line in logo:
        print(color + line)
        time.sleep(0.08)

    print(Style.RESET_ALL)

    if is_birthday():
        print(Fore.YELLOW + "🎂 Happy Birthday from PythOS!\n")

# ======================
# SIGNATURE
# ======================

def verify_signature():
    try:
        with open(sys.argv[0], "rb") as f:
            hashlib.sha256(f.read()).hexdigest()
        return True
    except:
        return False

# ======================
# BOOT FAILURE
# ======================

def boot_fail():

    clear()
    play(FAIL_SOUND)

    print(Fore.RED + "BOOT FAILURE")
    print("System halted.")

    input("Press ENTER")
    sys.exit()

# ======================
# BOOT
# ======================

def boot():

    clear()

    play(BOOT_SOUND)

    slow("Initializing firmware...",0.01)
    slow("Checking memory........OK",0.01)
    slow("Loading system...",0.01)

    if not verify_signature():
        boot_fail()

    show_logo()

    print(Fore.CYAN + "Welcome to")
    print("====== PythOS ======")
    print("Version", VERSION)
    print(Style.RESET_ALL)

    time.sleep(1)

# ======================
# CALCULATOR
# ======================

def calculator():

    clear()

    print(Fore.YELLOW + "Calculator\n")

    while True:

        expr = input("calc> ")

        if expr == "exit":
            break

        try:
            print("=", eval(expr))
        except:
            print("Invalid")

# ======================
# TIMER
# ======================

def timer():

    clear()

    seconds = int(input("Seconds: "))

    while seconds > 0:

        print("Time left:", seconds)
        time.sleep(1)
        seconds -= 1

    print("Time's up!")

    input()

# ======================
# NOTES
# ======================

def notes():

    clear()

    print("Write note (type SAVE to finish)\n")

    text = []

    while True:

        line = input()

        if line == "SAVE":
            break

        text.append(line)

    with open("pythos_notes.txt","w") as f:
        for l in text:
            f.write(l+"\n")

    print("Saved.")

    input()

# ======================
# SYSTEM INFO
# ======================

def system_info():

    clear()

    print(Fore.GREEN + "System Info\n")

    print("OS: PythOS")
    print("Version:",VERSION)
    print("Python:",sys.version.split()[0])
    print("Platform:",sys.platform)

    input()

# ======================
# UPDATES
# ======================

def updates():

    clear()

    print("Checking updates...\n")

    time.sleep(1)

    print(Fore.GREEN + "System up to date.")

    input()

# ======================
# MENU NAVIGATION
# ======================

import msvcrt

def arrow_menu(title, options):

    index = 0

    while True:

        clear()

        print(Fore.CYAN + title + "\n")

        for i,opt in enumerate(options):

            if i == index:
                print(Back.WHITE + Fore.BLACK + opt + Style.RESET_ALL)
            else:
                print(Fore.CYAN + opt)

        key = msvcrt.getch()

        if key == b'H':   # up
            index = (index - 1) % len(options)

        elif key == b'P': # down
            index = (index + 1) % len(options)

        elif key == b'\r':
            return index

# ======================
# TOOLS
# ======================

def tools():

    while True:

        choice = arrow_menu("Tools",[
            "Calculator",
            "Timer",
            "Notes",
            "System Info",
            "Back"
        ])

        if choice == 0:
            calculator()

        elif choice == 1:
            timer()

        elif choice == 2:
            notes()

        elif choice == 3:
            system_info()

        elif choice == 4:
            return

# ======================
# ABOUT
# ======================

def about():

    clear()

    print(Fore.CYAN + "About\n")

    print("PythOS Experimental System")
    print("Version:",VERSION)
    print("Edition: Stable Edition")
    print("\nDesigned by Kiteos Labs")

    input()

# ======================
# MAIN MENU
# ======================

def menu():

    while True:

        choice = arrow_menu("PythOS "+VERSION,[
            "Tools",
            "Check Updates",
            "About",
            "Shutdown"
        ])

        if choice == 0:
            tools()

        elif choice == 1:
            updates()

        elif choice == 2:
            about()

        elif choice == 3:
            clear()
            print("Shutting down PythOS...")
            time.sleep(1)
            break

# ======================
# MAIN
# ======================

if __name__ == "__main__":

    boot()
    menu()
