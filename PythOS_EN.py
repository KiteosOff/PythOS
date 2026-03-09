import os
import time
import platform
import msvcrt
from colorama import Fore, Back, Style, init

init()
os.system("")

VERSION = "1.4.6SE"


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def boot():

    clear()

    print(Fore.GREEN)
    print("Booting PythOS...")
    time.sleep(1)

    logo = [
"██████╗ ██╗   ██╗████████╗██╗  ██╗ ██████╗ ███████╗",
"██╔══██╗╚██╗ ██╔╝╚══██╔══╝██║  ██║██╔═══██╗██╔════╝",
"██████╔╝ ╚████╔╝    ██║   ███████║██║   ██║███████╗",
"██╔═══╝   ╚██╔╝     ██║   ██╔══██║██║   ██║╚════██║",
"██║        ██║      ██║   ██║  ██║╚██████╔╝███████║",
"╚═╝        ╚═╝      ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚══════╝"
    ]

    for line in logo:
        print(line)
        time.sleep(0.1)

    print(Style.RESET_ALL)
    time.sleep(1)


def arrow_menu(title, options, color):

    index = 0

    while True:

        clear()

        print(color + title + "\n" + Style.RESET_ALL)

        for i, opt in enumerate(options):

            if i == index:
                print(Back.WHITE + Fore.BLACK + opt + Style.RESET_ALL)
            else:
                print(color + opt + Style.RESET_ALL)

        key = msvcrt.getch()

        if key == b'\xe0':
            key = msvcrt.getch()

            if key == b'H':
                index = (index - 1) % len(options)

            elif key == b'P':
                index = (index + 1) % len(options)

        elif key == b'\r':
            return index


def calculator():

    while True:

        clear()
        print(Fore.YELLOW + "Calculator (type 'exit' to leave)\n")

        expr = input("> ")

        if expr.lower() == "exit":
            return

        try:
            result = eval(expr)
            print("=", result)
        except:
            print("Error")

        input("Press Enter...")


def timer():

    clear()
    print(Fore.GREEN + "Timer\n")

    try:
        seconds = int(input("Seconds: "))
    except:
        return

    for i in range(seconds, 0, -1):
        clear()
        print(Fore.GREEN + f"Timer: {i}")
        time.sleep(1)

    print("Time's up!")
    input("Press Enter...")


def notes():

    clear()
    print(Fore.BLUE + "Notes\n")

    note = input("Write note: ")

    with open("pythos_notes.txt", "a") as f:
        f.write(note + "\n")

    print("Saved.")
    input("Press Enter...")


def system_info():

    clear()

    print(Fore.CYAN + "System Info\n")

    print("System:", platform.system())
    print("Release:", platform.release())
    print("Machine:", platform.machine())
    print("Processor:", platform.processor())

    input("\nPress Enter...")


def updates():

    clear()

    print(Fore.CYAN + "Checking updates...\n")

    time.sleep(2)

    print("You are running the latest version.")
    input("Press Enter...")


def about():

    clear()

    print(Fore.MAGENTA + "About PythOS\n")

    print("Version:", VERSION)
    print("A mini terminal OS made in Python.")

    input("\nPress Enter...")


def tools():

    while True:

        choice = arrow_menu(
            "Tools",
            ["Calculator", "Timer", "Notes", "System Info", "Back"],
            Fore.MAGENTA
        )

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


def menu():

    while True:

        choice = arrow_menu(
            "PythOS " + VERSION,
            ["Tools", "Check Updates", "About", "Shutdown"],
            Fore.CYAN
        )

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


boot()
menu()
