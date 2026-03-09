import os
import time
import hashlib
import sys
import winsound
from colorama import Fore, Style, init

init()

VERSION = "1.4.6SE"

BOOT_SOUND = "pythos_boot.wav"
FAIL_SOUND = "pythos_bootfailure.wav"

# ========================
# UTIL
# ========================

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def slow(text, speed=0.015):
    for c in text:
        print(c, end="", flush=True)
        time.sleep(speed)
    print()

def play(sound):
    if os.path.exists(sound):
        winsound.PlaySound(sound, winsound.SND_FILENAME)

# ========================
# LOGO ASCII
# ========================

def show_logo():

    logo = [
"██████╗ ██╗   ██╗████████╗██╗  ██╗ ██████╗ ███████╗",
"██╔══██╗╚██╗ ██╔╝╚══██╔══╝██║  ██║██╔═══██╗██╔════╝",
"██████╔╝ ╚████╔╝    ██║   ███████║██║   ██║███████╗",
"██╔═══╝   ╚██╔╝     ██║   ██╔══██║██║   ██║╚════██║",
"██║        ██║      ██║   ██║  ██║╚██████╔╝███████║",
"╚═╝        ╚═╝      ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚══════╝"
]

    print()

    for line in logo:
        print(Fore.CYAN + line + Style.RESET_ALL)
        time.sleep(0.08)

    print(Fore.GREEN + "\nExperimental Python Operating Shell\n" + Style.RESET_ALL)

# ========================
# SIGNATURE
# ========================

def verify_signature():
    try:
        with open(sys.argv[0], "rb") as f:
            data = f.read()
            hashlib.sha256(data).hexdigest()
        return True
    except:
        return False

# ========================
# BOOT FAILURE
# ========================

def boot_fail():

    clear()
    play(FAIL_SOUND)

    print(Fore.RED + "\nBOOT FAILURE")
    print("System halted." + Style.RESET_ALL)

    input("\nPress ENTER to exit.")
    sys.exit()

# ========================
# BOOT
# ========================

def boot():

    clear()

    play(BOOT_SOUND)

    slow("Initializing firmware...", 0.01)
    slow("Checking memory........OK", 0.01)
    slow("Loading system...", 0.01)

    if not verify_signature():
        boot_fail()

    show_logo()

    print(Fore.CYAN + "Welcome to")
    print("====== PythOS ======")
    print("Version", VERSION + Style.RESET_ALL)
    print()

    time.sleep(1)

# ========================
# CALCULATOR
# ========================

def calculator():

    clear()

    print(Fore.YELLOW + "PythOS Calculator")
    print("Type 'exit' to return\n" + Style.RESET_ALL)

    while True:

        expr = input("calc> ")

        if expr.lower() == "exit":
            break

        try:
            print("=", eval(expr))
        except:
            print("Invalid expression")

# ========================
# SYSTEM INFO
# ========================

def system_info():

    clear()

    print(Fore.GREEN + "System Information\n" + Style.RESET_ALL)

    print("OS:", "PythOS")
    print("Version:", VERSION)
    print("Python:", sys.version.split()[0])
    print("Platform:", sys.platform)

    input("\nPress ENTER to return")

# ========================
# UPDATES
# ========================

def updates():

    clear()

    print("Checking for updates...\n")
    time.sleep(1)

    latest = "1.4.6SE"

    if latest == VERSION:
        print(Fore.GREEN + "System up to date." + Style.RESET_ALL)
    else:
        print(Fore.YELLOW + "Update available:", latest + Style.RESET_ALL)

    input("\nPress ENTER to return")

# ========================
# TOOLS MENU
# ========================

def tools():

    while True:

        clear()

        print(Fore.MAGENTA + "PythOS Tools\n" + Style.RESET_ALL)

        print("1 - Calculator")
        print("2 - System Info")
        print("3 - Back")
        print()

        c = input("> ")

        if c == "1":
            calculator()

        elif c == "2":
            system_info()

        elif c == "3":
            break

# ========================
# ABOUT
# ========================

def about():

    clear()

    print(Fore.CYAN + "About PythOS\n" + Style.RESET_ALL)

    print("PythOS Experimental System")
    print("Version:", VERSION)
    print("Edition: Stable Edition")
    print()
    print("Designed by Kiteos Labs")

    input("\nPress ENTER to return")

# ========================
# MAIN MENU
# ========================

def menu():

    while True:

        clear()

        print(Fore.CYAN + "PythOS", VERSION + Style.RESET_ALL)
        print("----------------------")

        print("1 - Tools")
        print("2 - Check for updates")
        print("3 - About")
        print("4 - Shutdown")
        print()

        choice = input("> ")

        if choice == "1":
            tools()

        elif choice == "2":
            updates()

        elif choice == "3":
            about()

        elif choice == "4":

            clear()
            print("Shutting down PythOS...")
            time.sleep(1)
            break

# ========================
# MAIN
# ========================

if __name__ == "__main__":

    boot()
    menu()
