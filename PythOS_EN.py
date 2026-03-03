import curses
import pickle
import os
import time
import urllib.request
import sys
import shutil

class PythOS:

    VERSION = "1.3.4"

    UPDATE_SCRIPT_URL = "https://raw.githubusercontent.com/KiteosOff/PythOS/main/PythOS_EN.py"
    UPDATE_VERSION_URL = "https://raw.githubusercontent.com/KiteosOff/PythOS/main/PythOSversion.txt"

    def __init__(self):
        self.state = "menu"
        self.current_selection = 0

        self.menu_items = [
            "Notes",
            "Timer",
            "Calculator",
            "User Config",
            "About",
            "Exit"
        ]

        self.notes = {}
        self.notes_selection = 0

        self.user = {"name": "", "birthday": ""}
        self.status_message = ""
        self.status_timer = 0
        self.status_color = 5

        self.load_notes()
        self.load_user()

        self.remote_version = None
        self.update_checked = False

    # ================= FILES =================

    def load_notes(self):
        if os.path.exists("notes.pkl"):
            try:
                with open("notes.pkl", "rb") as f:
                    self.notes = pickle.load(f)
            except:
                self.notes = {}

    def save_notes(self):
        with open("notes.pkl", "wb") as f:
            pickle.dump(self.notes, f)

    def load_user(self):
        if os.path.exists("userconfig.pkl"):
            try:
                with open("userconfig.pkl", "rb") as f:
                    self.user = pickle.load(f)
            except:
                pass

    def save_user(self):
        with open("userconfig.pkl", "wb") as f:
            pickle.dump(self.user, f)

    # ================= UPDATE =================

    def parse_version(self, v):
        return tuple(map(int, v.split(".")))

    def check_update(self):
        try:
            with urllib.request.urlopen(self.UPDATE_VERSION_URL, timeout=3) as r:
                return r.read().decode().strip()
        except:
            return None

    def backup_current(self):
        shutil.copy(__file__, "PythOS_backup.py")

    def restore_backup(self):
        if os.path.exists("PythOS_backup.py"):
            shutil.copy("PythOS_backup.py", __file__)

    def download_update(self):
        try:
            self.backup_current()

            with urllib.request.urlopen(self.UPDATE_SCRIPT_URL) as r:
                new_code = r.read().decode()

            with open(__file__, "w", encoding="utf-8") as f:
                f.write(new_code)

            os.execv(sys.executable, [sys.executable] + sys.argv)

        except:
            self.restore_backup()
            self.show_status("Update failed – restored backup", 4)

    # ================= STATUS =================

    def show_status(self, message, color_pair=5):
        self.status_message = message
        self.status_timer = 60
        self.status_color = color_pair

    # ================= DRAW =================

    def draw_menu(self, stdscr):
        title = f"PythOS {self.VERSION}"

        if self.remote_version:
            local = self.parse_version(self.VERSION)
            remote = self.parse_version(self.remote_version)
            if remote > local:
                title += f" | Update {self.remote_version} available (U)"

        stdscr.addstr(1, 2, title, curses.A_BOLD)

        colors = {
            "Notes": 1,
            "Timer": 2,
            "Calculator": 3,
            "User Config": 7,
            "About": 6,
            "Exit": 4
        }

        for idx, item in enumerate(self.menu_items):
            color = curses.color_pair(colors[item])
            if idx == self.current_selection:
                stdscr.addstr(3 + idx, 4, item, color | curses.A_REVERSE)
            else:
                stdscr.addstr(3 + idx, 4, item, color)

    # ================= MAIN =================

    def run(self, stdscr):

        curses.curs_set(0)
        curses.start_color()

        curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(6, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        curses.init_pair(7, curses.COLOR_CYAN, curses.COLOR_BLACK)

        stdscr.timeout(100)

        if not self.update_checked:
            self.remote_version = self.check_update()
            self.update_checked = True

        # Birthday check
        today = time.strftime("%d/%m")
        if self.user["birthday"] == today and self.user["name"]:
            self.show_status(f"🎉 Happy Birthday, {self.user['name']}! 🎉", 1)

        while True:
            stdscr.clear()
            self.draw_menu(stdscr)

            if self.status_timer > 0:
                h, _ = stdscr.getmaxyx()
                stdscr.addstr(h - 2, 2, self.status_message,
                              curses.color_pair(self.status_color))
                self.status_timer -= 1

            stdscr.refresh()
            key = stdscr.getch()

            if key in (ord('u'), ord('U')) and self.remote_version:
                local = self.parse_version(self.VERSION)
                remote = self.parse_version(self.remote_version)
                if remote > local:
                    self.download_update()

            if key == curses.KEY_UP and self.current_selection > 0:
                self.current_selection -= 1
            elif key == curses.KEY_DOWN and self.current_selection < len(self.menu_items)-1:
                self.current_selection += 1
            elif key == 10:
                choice = self.menu_items[self.current_selection]

                if choice == "User Config":
                    self.edit_user(stdscr)
                elif choice == "Exit":
                    return
                else:
                    self.show_status("Feature in development", 4)

    # ================= USER CONFIG =================

    def edit_user(self, stdscr):
        curses.echo()
        stdscr.clear()
        stdscr.addstr(2, 2, "User Configuration", curses.A_BOLD)

        stdscr.addstr(4, 2, f"Current Name: {self.user['name']}")
        stdscr.addstr(5, 2, "Enter new name: ")
        name = stdscr.getstr(5, 20, 20).decode()

        stdscr.addstr(7, 2, f"Current Birthday: {self.user['birthday']}")
        stdscr.addstr(8, 2, "Enter birthday (DD/MM): ")
        birthday = stdscr.getstr(8, 28, 5).decode()

        if name:
            self.user["name"] = name

        if birthday:
            try:
                time.strptime(birthday, "%d/%m")
                self.user["birthday"] = birthday
            except:
                self.show_status("Invalid birthday format", 4)

        self.save_user()
        curses.noecho()
        self.show_status("User config saved", 7)


def main():
    osys = PythOS()
    curses.wrapper(osys.run)


if __name__ == "__main__":
    main()

