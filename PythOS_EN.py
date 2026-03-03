import curses
import pickle
import os
import time
import urllib.request
import sys
import shutil
import platform

if platform.system() == "Windows":
    import winsound


class PythOS:

    VERSION = "1.3.9"

    UPDATE_VERSION_URL = "https://raw.githubusercontent.com/KiteosOff/PythOS/main/PythOSversion.txt"
    UPDATE_SCRIPT_URL = "https://raw.githubusercontent.com/KiteosOff/PythOS/main/PythOS_EN.py"

    def __init__(self):
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

        self.updated_flag = False

    # ================= SOUND =================

    def soft_beep(self):
        if platform.system() == "Windows":
            winsound.Beep(800, 40)
        else:
            curses.beep()

    def futuristic_boot_sound(self):
        if platform.system() == "Windows":
            winsound.Beep(600, 80)
            winsound.Beep(750, 100)
            winsound.Beep(900, 120)
        else:
            curses.beep()

    def fatal_sound(self):
        if platform.system() == "Windows":
            winsound.Beep(400, 150)
            time.sleep(0.1)
            winsound.Beep(300, 300)
        else:
            curses.beep()
            time.sleep(0.1)
            curses.beep()

    # ================= FILES =================

    def load_user(self):
        if os.path.exists("userconfig.pkl"):
            try:
                with open("userconfig.pkl", "rb") as f:
                    self.user = pickle.load(f)
            except:
                self.user = {"name": "", "birthday": ""}

    def save_user(self):
        with open("userconfig.pkl", "wb") as f:
            pickle.dump(self.user, f)

    # ================= UPDATE =================

    def backup_script(self):
        shutil.copyfile(__file__, __file__ + ".bak")

    def restore_backup(self):
        if os.path.exists(__file__ + ".bak"):
            shutil.copyfile(__file__ + ".bak", __file__)

    def check_for_updates(self):
        try:
            with urllib.request.urlopen(self.UPDATE_VERSION_URL, timeout=3) as response:
                latest_version = response.read().decode().strip()

            if latest_version != self.VERSION:
                return latest_version
        except:
            return None

        return None

    def apply_update(self, latest_version):
        try:
            self.backup_script()

            with urllib.request.urlopen(self.UPDATE_SCRIPT_URL, timeout=5) as response:
                new_code = response.read().decode()

            with open(__file__, "w", encoding="utf-8") as f:
                f.write(new_code)

            self.updated_flag = True
            os.execv(sys.executable, ['python'] + sys.argv)

        except:
            self.restore_backup()

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

        self.futuristic_boot_sound()

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

        time.sleep(0.5)

    # ================= SYSTEM CHECK =================

    def system_check(self, stdscr):

        height, width = stdscr.getmaxyx()

        checks = [
            "Checking notes file...",
            "Checking user config...",
            "Checking write permissions...",
            "Checking update server...",
            "Verifying core..."
        ]

        success = True

        for i, check in enumerate(checks):

            stdscr.clear()

            percent = int((i / len(checks)) * 100)
            bar_length = 20
            filled = int((i / len(checks)) * bar_length)
            bar = "█" * filled + "░" * (bar_length - filled)

            stdscr.addstr(height//2 - 2,
                          (width - len("System Check"))//2,
                          "System Check",
                          curses.A_BOLD)

            stdscr.addstr(height//2,
                          (width - len(check))//2,
                          check)

            stdscr.addstr(height//2 + 2,
                          (width - len(bar) - 6)//2,
                          f"[{bar}] {percent}%")

            stdscr.refresh()
            time.sleep(0.3)

            try:
                if i == 0:
                    if not os.path.exists("notes.pkl"):
                        open("notes.pkl", "wb").close()

                elif i == 1:
                    if not os.path.exists("userconfig.pkl"):
                        open("userconfig.pkl", "wb").close()

                elif i == 2:
                    with open("test.tmp", "w") as f:
                        f.write("ok")
                    os.remove("test.tmp")

                elif i == 3:
                    urllib.request.urlopen(self.UPDATE_VERSION_URL, timeout=2)

                elif i == 4:
                    if not os.path.exists(__file__):
                        success = False

                self.soft_beep()

            except:
                success = False

        stdscr.clear()
        bar = "█" * 20

        stdscr.addstr(height//2,
                      (width - 28)//2,
                      f"[{bar}] 100%")

        if success:
            stdscr.addstr(height//2 + 2,
                          (width - 9)//2,
                          "SYSTEM OK",
                          curses.color_pair(3))
        else:
            stdscr.addstr(height//2 + 2,
                          (width - 14)//2,
                          "BOOT FAILURE",
                          curses.color_pair(4))
            self.fatal_sound()

        stdscr.refresh()
        time.sleep(1.5)

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

            elif key in (10, 13) and not running:
                running = True
                start_time = time.time() - seconds

            elif key == 32 and running:
                running = False

            elif key in (ord('r'), ord('R')):
                running = False
                seconds = 0

    # ================= USER CONFIG =================

    def edit_user(self, stdscr):

        curses.echo()
        curses.curs_set(1)
        stdscr.clear()

        stdscr.addstr(2, 2, "User Configuration", curses.color_pair(2) | curses.A_BOLD)

        stdscr.addstr(4, 2, "Name: ")
        name = stdscr.getstr(4, 8, 20).decode("utf-8")

        stdscr.addstr(6, 2, "Birthday (DD/MM): ")
        birthday = stdscr.getstr(6, 22, 5).decode("utf-8")

        curses.noecho()
        curses.curs_set(0)

        if name:
            self.user["name"] = name

        if birthday and len(birthday) == 5 and birthday[2] == "/":
            self.user["birthday"] = birthday

        self.save_user()

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

        latest = self.check_for_updates()
        if latest:
            self.apply_update(latest)

        self.splash(stdscr)
        self.system_check(stdscr)

        stdscr.timeout(100)

        while True:

            stdscr.clear()
            stdscr.addstr(1, 2, f"PythOS {self.VERSION}", curses.A_BOLD)

            colors = {
                "Notes": 1,
                "Timer": 2,
                "Calculator": 3,
                "User Config": 2,
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

            stdscr.refresh()
            key = stdscr.getch()

            if key == curses.KEY_UP and self.current_selection > 0:
                self.current_selection -= 1

            elif key == curses.KEY_DOWN and self.current_selection < len(self.menu_items)-1:
                self.current_selection += 1

            elif key in (10, 13):
                choice = self.menu_items[self.current_selection]

                if choice == "Timer":
                    self.timer_screen(stdscr)

                elif choice == "User Config":
                    self.edit_user(stdscr)

                elif choice == "Exit":
                    return


def main():
    osys = PythOS()
    curses.wrapper(osys.run)


if __name__ == "__main__":
    main()
