import os
import time
import hashlib
import winsound
import sys

VERSION = "1.4.4-BSE"
BUILD_ID = "042"

BOOT_SOUND = "pythos_boot.wav"
FAIL_SOUND = "pythos_bootfailure.wav"

# ==============================
# UTILITAIRES
# ==============================

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def slow_print(text, delay=0.02):
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()

def play_sound(file):
    if os.path.exists(file):
        winsound.PlaySound(file, winsound.SND_FILENAME)
    else:
        pass  # silencieux si absent

# ==============================
# BOOT SIGNATURE
# ==============================

def verify_boot_signature():
    slow_print("Verifying Boot Signature...", 0.01)
    time.sleep(0.5)

    # Hash du fichier courant
    try:
        with open(sys.argv[0], "rb") as f:
            data = f.read()
            file_hash = hashlib.sha256(data).hexdigest()[:16]
        slow_print("Signature OK")
        slow_print(f"Build ID: {BUILD_ID}")
        slow_print(f"Hash: {file_hash}")
        return True
    except:
        slow_print("Signature FAILED")
        return False

# ==============================
# BOOT SCREEN
# ==============================

def boot_screen():
    clear()
    slow_print("Initializing firmware...", 0.01)
    time.sleep(0.4)
    slow_print("Checking memory........OK", 0.01)
    time.sleep(0.3)

    if not verify_boot_signature():
        boot_failure()
        return False

    print()
    slow_print("Welcome to", 0.03)
    slow_print("======  PythOS  ======", 0.03)
    slow_print(f"      {VERSION}", 0.03)
    print()
    slow_print("Boot Integrity: VALID", 0.02)
    slow_print("Core Status: STABLE", 0.02)
    time.sleep(1)

    return True

# ==============================
# BOOT FAILURE
# ==============================

def boot_failure():
    play_sound(FAIL_SOUND)
    print("\nFATAL BOOT ERROR")
    print("System Halted.")
    input("Press ENTER to exit...")
    sys.exit()

# ==============================
# CALCULATRICE
# ==============================

def calculator():
    clear()
    print("=== PythOS Calculator ===")
    print("Type 'exit' to return\n")

    while True:
        expr = input(">>> ")
        if expr.lower() == "exit":
            break
        try:
            result = eval(expr)
            print("=", result)
        except:
            print("Invalid expression")

# ==============================
# UPDATE CHECK
# ==============================

def check_updates():
    clear()
    print("=== Checking for updates ===\n")
    time.sleep(1)

    # Simulation locale
    latest_version = "1.4.4-BSE"

    if latest_version != VERSION:
        print("Update available:", latest_version)
    else:
        print("Your system is up to date.")

    input("\nPress ENTER to return...")

# ==============================
# SHELL
# ==============================

def shell():
    while True:
        clear()
        print(f"PythOS {VERSION}")
        print("======================")
        print("1. Calculator")
        print("2. Check for updates")
        print("3. Exit")
        print()

        choice = input("Select option: ")

        if choice == "1":
            calculator()
        elif choice == "2":
            check_updates()
        elif choice == "3":
            clear()
            print("Shutting down PythOS...")
            time.sleep(1)
            break
        else:
            print("Invalid option")
            time.sleep(1)

# ==============================
# MAIN
# ==============================

if __name__ == "__main__":
    play_sound(BOOT_SOUND)

    if boot_screen():
        shell()
