import os
import time
import hashlib
import winsound
import sys

VERSION = "1.4.5SE"

BOOT_SOUND = "pythos_boot.wav"
FAIL_SOUND = "pythos_bootfailure.wav"


# ======================
# UTILITAIRES
# ======================

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def slow(text, speed=0.02):
    for c in text:
        print(c, end="", flush=True)
        time.sleep(speed)
    print()

def play(sound):
    if os.path.exists(sound):
        winsound.PlaySound(sound, winsound.SND_FILENAME)


# ======================
# BOOT SIGNATURE
# ======================

def verify_signature():
    try:
        with open(sys.argv[0], "rb") as f:
            data = f.read()
            hashlib.sha256(data).hexdigest()
        return True
    except:
        return False


# ======================
# BOOT FAILURE
# ======================

def boot_fail():
    play(FAIL_SOUND)
    print("\nBOOT FAILURE")
    print("System halted.")
    input("\nPress ENTER to exit.")
    sys.exit()


# ======================
# BOOT SCREEN
# ======================

def boot():

    clear()

    slow("Initializing firmware...", 0.01)
    time.sleep(0.4)

    slow("Checking memory........OK", 0.01)
    time.sleep(0.3)

    slow("Loading system...", 0.01)
    time.sleep(0.4)

    if not verify_signature():
        boot_fail()

    print()
    print("Welcome to")
    print("====== PythOS ======")
    print("Version", VERSION)
    print()

    time.sleep(1)


# ======================
# CALCULATOR
# ======================

def calculator():

    clear()

    print("PythOS Calculator")
    print("Type 'exit' to return\n")

    while True:

        expr = input("calc> ")

        if expr.lower() == "exit":
            break

        try:
            print("=", eval(expr))
        except:
            print("Invalid expression")


# ======================
# UPDATE CHECK
# ======================

def updates():

    clear()

    print("Checking for updates...\n")
    time.sleep(1)

    latest = "1.4.4"

    if latest == VERSION:
        print("System up to date.")
    else:
        print("Update available:", latest)

    input("\nPress ENTER to return")


# ======================
# MENU
# ======================

def menu():

    while True:

        clear()

        print("PythOS", VERSION)
        print("-------------------")
        print("1 - Calculator")
        print("2 - Check for updates")
        print("3 - Shutdown")
        print()

        choice = input("> ")

        if choice == "1":
            calculator()

        elif choice == "2":
            updates()

        elif choice == "3":
            clear()
            print("Shutting down PythOS...")
            time.sleep(1)
            break


# ======================
# MAIN
# ======================

if __name__ == "__main__":

    play(BOOT_SOUND)

    boot()

    menu()
