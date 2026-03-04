# -*- coding: utf-8 -*-

import curses
import pickle
import os
import time
import sys
import platform
import urllib.request

if platform.system() == "Windows":
    import winsound


class PythOS:

    VERSION = "1.4.2"

    UPDATE_VERSION_URL = "https://raw.githubusercontent.com/KiteosOff/PythOS/main/PythOSversion.txt"
    UPDATE_SCRIPT_URL = "https://raw.githubusercontent.com/KiteosOff/PythOS/main/PythOS_EN.py"

    def __init__(self):
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        self.notes_file = os.path.join(self.base_path, "notes.pkl")
        self.user_file = os.path.join(self.base_path, "userconfig.pkl")

        self.menu_items = [
            "Notes",
            "Timer",
            "Calculator",
            "User Config",
            "About",
            "Exit"
        ]

        self.current_selection = 0
        self.user = {"name": "", "birthday": ""}
        self.load_user()

    # ================= SOUND =================

    def soft_beep(self):
        if platform.system() == "Windows":
            winsound.Beep(900, 30)
        else:
            curses.beep()

    # ================= FILES =================

    def load_user(self):
        if os.path.exists(self.user_file):
            try:
                with open(self.user_file, "rb") as f:
                    self.user = pickle.load(f)
            except:
                self.user = {"name": "", "birthday": ""}
        else:
            self.save_user()

    def save_user(self):
        with open(self.user_file, "wb") as f:
            pickle.dump(self.user, f)

    def load_notes(self):
        if os.path.exists(self.notes_file):
            try:
                with open(self.notes_file, "rb") as f:
                    return pickle.load(f)
            except:
                return []
        else:
            self.save_notes([])
            return []

    def save_notes(self, notes):
        with open(self.notes_file, "wb") as f:
            pickle.dump(notes, f)

    # ================= SYSTEM CHECK =================

    def system_check(self, stdscr):
        stdscr.clear()
        stdscr.addstr(2, 2, "System check...", curses.A_BOLD)
        stdscr.refresh()
        time.sleep(0.8)

        try:
            if not os.path.exists(self.notes_file):
                self.save_notes([])
            if not os.path.exists(self.user_file):
                self.save_user()
        except Exception as e:
            stdscr.addstr(4, 2, "Storage Warning", curses.color_pair(4))
            stdscr.addstr(6, 2, str(e))
            stdscr.refresh()
            stdscr.getch()

    # ================= NOTES =================

    def notes_screen(self, stdscr):

        notes = self.load_notes()

        while True:
            stdscr.clear()
            stdscr.addstr(1, 2, "Notes", curses.A_BOLD)

            for i, note in enumerate(notes):
                stdscr.addstr(3 + i, 4, f"- {note}")

            stdscr.addstr(15, 2, "A=Add  D=Delete last  ESC=Back")
            stdscr.refresh()

            key = stdscr.getch()

            if key == 27:
                break

            elif key in (ord('a'), ord('A')):
                curses.echo()
                stdscr.addstr(17, 2, "New note: ")
                note = stdscr.getstr(17, 12, 60).decode("utf-8", errors="ignore")
                curses.noecho()
                if note:
                    notes.append(note)
                    self.save_notes(notes)

            elif key in (ord('d'), ord('D')):
                if notes:
                    notes.pop()
                    self.save_notes(notes)

    # ================= TIMER =================

    def timer_screen(self, stdscr):

        running = False
        seconds = 0
        start_time = 0
        stdscr.timeout(100)

        while True:
            stdscr.clear()
            height, width = stdscr.getmaxyx()

            if running:
                seconds = int(time.time() - start_time)

            mins = seconds // 60
            secs = seconds % 60
            time_str = f"{mins:02}:{secs:02}"

            stdscr.addstr(height//2,
                          (width - len(time_str))//2,
                          time_str,
                          curses.color_pair(2) | curses.A_BOLD)

            stdscr.addstr(height-2, 2,
                          "ENTER=Start  SPACE=Pause  R=Reset  ESC=Back")

            stdscr.refresh()
            key = stdscr.getch()

            if key == 27:
                break
            elif key in (10, 13, curses.KEY_ENTER) and not running:
                running = True
                start_time = time.time() - seconds
            elif key == 32 and running:
                running = False
            elif key in (ord('r'), ord('R')):
                running = False
                seconds = 0

    # ================= CALCULATOR =================

    def calculator_screen(self, stdscr):

        curses.echo()
        curses.curs_set(1)

        while True:
            stdscr.clear()
            stdscr.addstr(2, 2, "Calculator (type 'exit' to leave)",
                          curses.color_pair(3) | curses.A_BOLD)
            stdscr.addstr(4, 2, ">>> ")

            stdscr.refresh()
            expr = stdscr.getstr(4, 6, 40).decode("utf-8", errors="ignore")

            if expr.lower() == "exit":
                break

            try:
                result = eval(expr)
                stdscr.addstr(6, 2, f"= {result}",
                              curses.color_pair(3))
            except:
                stdscr.addstr(6, 2, "Invalid expression",
                              curses.color_pair(4))
                self.soft_beep()

            stdscr.refresh()
            stdscr.getch()

        curses.noecho()
        curses.curs_set(0)

    # ================= USER CONFIG =================

    def user_config_screen(self, stdscr):

        while True:
            stdscr.clear()
            stdscr.addstr(2, 2, "User Configuration", curses.A_BOLD)

            stdscr.addstr(4, 4, f"Name: {self.user['name']}")
            stdscr.addstr(5, 4, f"Birthday: {self.user['birthday']}")

            stdscr.addstr(7, 4, "E = Edit")
            stdscr.addstr(8, 4, "ESC = Back")

            stdscr.refresh()
            key = stdscr.getch()

            if key == 27:
                break
            elif key in (ord('e'), ord('E')):
                self.edit_user(stdscr)

    def edit_user(self, stdscr):

        curses.echo()
        curses.curs_set(1)

        stdscr.clear()
        stdscr.addstr(2, 2, "Edit User", curses.A_BOLD)

        stdscr.addstr(4, 2, "Name: ")
        name = stdscr.getstr(4, 8, 20).decode("utf-8", errors="ignore")

        stdscr.addstr(6, 2, "Birthday (DD/MM): ")
        birthday = stdscr.getstr(6, 22, 5).decode("utf-8", errors="ignore")

        curses.noecho()
        curses.curs_set(0)

        if name:
            self.user["name"] = name
        if birthday and len(birthday) == 5 and birthday[2] == "/":
            self.user["birthday"] = birthday

        self.save_user()

    # ================= ABOUT =================

    def about_screen(self, stdscr):

        while True:
            stdscr.clear()
            stdscr.addstr(2, 2, "About PythOS", curses.A_BOLD)
            stdscr.addstr(4, 4, f"Version: {self.VERSION}")
            stdscr.addstr(5, 4, "Developer: KiteosOff")

            stdscr.addstr(7, 4, "U = Check for updates")
            stdscr.addstr(8, 4, "ESC = Back")

            stdscr.refresh()
            key = stdscr.getch()

            if key == 27:
                break

            elif key in (ord('u'), ord('U')):
                stdscr.addstr(10, 4, "Checking...")
                stdscr.refresh()
                time.sleep(1)

    # ================= MAIN =================

    def run(self, stdscr):

        curses.curs_set(0)
        curses.start_color()
        stdscr.keypad(True)

        curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)

        self.system_check(stdscr)

        while True:

            stdscr.clear()
            stdscr.addstr(1, 2, f"PythOS {self.VERSION}",
                          curses.A_BOLD)

            for i, item in enumerate(self.menu_items):

                if item == "Exit":
                    color = curses.color_pair(4)
                else:
                    color = curses.color_pair((i % 3) + 1)

                if i == self.current_selection:
                    stdscr.addstr(3+i, 4, item,
                                  color | curses.A_REVERSE)
                else:
                    stdscr.addstr(3+i, 4, item, color)

            stdscr.refresh()
            key = stdscr.getch()

            if key == curses.KEY_UP and self.current_selection > 0:
                self.current_selection -= 1
            elif key == curses.KEY_DOWN and self.current_selection < len(self.menu_items)-1:
                self.current_selection += 1
            elif key in (10, 13, curses.KEY_ENTER):

                choice = self.menu_items[self.current_selection]

                if choice == "Notes":
                    self.notes_screen(stdscr)
                elif choice == "Timer":
                    self.timer_screen(stdscr)
                elif choice == "Calculator":
                    self.calculator_screen(stdscr)
                elif choice == "User Config":
                    self.user_config_screen(stdscr)
                elif choice == "About":
                    self.about_screen(stdscr)
                elif choice == "Exit":
                    return


def main():
    try:
        osys = PythOS()
        curses.wrapper(osys.run)
    except Exception as e:
        print("CRASH DETECTED:")
        print(e)
        input("Press ENTER to exit...")


if __name__ == "__main__":
    main()
