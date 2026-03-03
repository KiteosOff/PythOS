import curses
import pickle
import os
import time
import urllib.request
import sys
import shutil


class PythOS:

    VERSION = "1.3.7"

    UPDATE_VERSION_URL = "https://raw.githubusercontent.com/KiteosOff/PythOS/main/PythOSversion.txt"
    UPDATE_SCRIPT_URL = "https://raw.githubusercontent.com/KiteosOff/PythOS/main/PythOS_EN.py"

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
        self.user = {"name": "", "birthday": ""}

        self.status_message = ""
        self.status_timer = 0
        self.status_color = 5

        # Timer
        self.timer_running = False
        self.timer_seconds = 0
        self.timer_start = 0

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

    # ================= SPLASH =================

    def splash(self, stdscr):

        height, width = stdscr.getmaxyx()

        today = time.strftime("%d/%m")
        is_birthday = (
            self.user["birthday"] == today and self.user["name"]
        )

        color = curses.color_pair(1) if is_birthday else curses.A_NORMAL

        text1 = "Welcome to"
        title = "PythOS"

        for i in range(4):
            stdscr.clear()

            stdscr.addstr(height//2 - 1,
                          (width - len(text1))//2,
                          text1,
                          color)

            animated = "=" * i + " " + title + " " + "=" * i

            stdscr.addstr(height//2,
                          (width - len(animated))//2,
                          animated,
                          color | curses.A_BOLD)

            stdscr.refresh()
            time.sleep(0.3)

        time.sleep(0.8)

    # ================= TIMER =================

    def timer_screen(self, stdscr):

        self.timer_running = False
        self.timer_seconds = 0

        stdscr.timeout(100)

        while True:

            stdscr.clear()
            height, width = stdscr.getmaxyx()

            if self.timer_running:
                self.timer_seconds = int(time.time() - self.timer_start)

            mins = self.timer_seconds // 60
            secs = self.timer_seconds % 60
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

            elif key == 10 and not self.timer_running:
                self.timer_running = True
                self.timer_start = time.time() - self.timer_seconds

            elif key == 32 and self.timer_running:
                self.timer_running = False

            elif key in (ord('r'), ord('R')):
                self.timer_running = False
                self.timer_seconds = 0

    # ================= USER CONFIG =================

    def edit_user(self, stdscr):

        curses.echo()
        curses.curs_set(1)
        stdscr.timeout(-1)

        stdscr.clear()
        stdscr.addstr(2, 2, "User Configuration", curses.A_BOLD)

        stdscr.addstr(4, 2, "Enter name: ")
        stdscr.refresh()
        name = stdscr.getstr(4, 15, 20).decode("utf-8")

        stdscr.addstr(6, 2, "Birthday (DD/MM): ")
        stdscr.refresh()
        birthday = stdscr.getstr(6, 22, 5).decode("utf-8")

        curses.noecho()
        curses.curs_set(0)
        stdscr.timeout(100)

        if name:
            self.user["name"] = name

        if birthday:
            if len(birthday) == 5 and birthday[2] == "/":
                self.user["birthday"] = birthday
            else:
                self.show_status("Invalid birthday format", 4)
                return

        self.save_user()
        self.show_status("User config saved", 7)

    # ================= MAIN LOOP =================

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

        self.splash(stdscr)

        stdscr.timeout(100)

        if not self.update_checked:
            self.remote_version = self.check_update()
            self.update_checked = True

        while True:

            stdscr.clear()
            stdscr.addstr(1, 2, f"PythOS {self.VERSION}", curses.A_BOLD)

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
                    stdscr.addstr(3 + idx, 4, item,
                                  color | curses.A_REVERSE)
                else:
                    stdscr.addstr(3 + idx, 4, item, color)

            if self.status_timer > 0:
                h, _ = stdscr.getmaxyx()
                stdscr.addstr(h - 2, 2,
                              self.status_message,
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

                if choice == "Timer":
                    self.timer_screen(stdscr)

                elif choice == "User Config":
                    self.edit_user(stdscr)

                elif choice == "Exit":
                    return

                else:
                    self.show_status("Feature in development", 4)


def main():
    osys = PythOS()
    curses.wrapper(osys.run)


if __name__ == "__main__":
    main()
