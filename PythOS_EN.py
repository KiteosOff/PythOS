import curses
import pickle
import os
import time
import urllib.request
import sys
from datetime import datetime


class PythOS:

    VERSION = "1.3.2"

    UPDATE_VERSION_URL = "https://raw.githubusercontent.com/KiteosOff/PythOS/main/PythOSversion.txt"
    UPDATE_SCRIPT_URL = "https://raw.githubusercontent.com/KiteosOff/PythOS/main/PythOS_EN.py"

    def __init__(self):
        self.state = "menu"
        self.current_selection = 0
        self.menu_items = ["Notes", "Timer", "Calculator", "Exit"]

        self.notes = {}
        self.notes_selection = 0

        self.current_note_name = ""
        self.current_note_content = ""

        self.cursor_x = 0
        self.cursor_y = 0
        self.scroll_offset = 0

        self.status_message = ""
        self.status_timer = 0
        self.status_color = 4

        self.last_auto_save = time.time()

        self.remote_version = None
        self.update_checked = False

        self.load_notes()

    # ================= VERSION SYSTEM =================

    def parse_version(self, v):
        return tuple(map(int, v.split(".")))

    def check_update(self):
        try:
            with urllib.request.urlopen(self.UPDATE_VERSION_URL, timeout=3) as r:
                return r.read().decode().strip()
        except:
            return None

    def download_update(self):
        try:
            with urllib.request.urlopen(self.UPDATE_SCRIPT_URL) as r:
                new_code = r.read().decode()

            with open(__file__, "w", encoding="utf-8") as f:
                f.write(new_code)

            os.execv(sys.executable, ['python'] + sys.argv)
        except:
            self.show_status("Update failed.", 4)

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

    # ================= DRAW =================

    def draw_menu(self, stdscr):
        title = f"PythOS {self.VERSION}"

        if self.remote_version:
            local = self.parse_version(self.VERSION)
            remote = self.parse_version(self.remote_version)

            if remote > local:
                title += f" | Update {self.remote_version} available (U)"

        stdscr.addstr(1, 2, title, curses.A_BOLD)

        for idx, item in enumerate(self.menu_items):
            if idx == self.current_selection:
                stdscr.addstr(3 + idx, 4, item, curses.A_REVERSE)
            else:
                stdscr.addstr(3 + idx, 4, item)

    def draw_notes_menu(self, stdscr):
        stdscr.addstr(1, 2, "Notes", curses.A_BOLD)
        stdscr.addstr(2, 2, "N=New  ENTER=Edit  ESC=Back")

        names = list(self.notes.keys())

        for idx, name in enumerate(names):
            if idx == self.notes_selection:
                stdscr.addstr(4 + idx, 4, name, curses.A_REVERSE)
            else:
                stdscr.addstr(4 + idx, 4, name)

    def draw_note_editor(self, stdscr):
        height, width = stdscr.getmaxyx()

        stdscr.addstr(0, 0, f"Editing: {self.current_note_name}", curses.A_BOLD)
        stdscr.addstr(1, 0, "ESC=Save & Exit  CTRL+S=Save")

        lines = self.current_note_content.split("\n")
        visible_height = height - 4

        if self.cursor_y < self.scroll_offset:
            self.scroll_offset = self.cursor_y
        elif self.cursor_y >= self.scroll_offset + visible_height:
            self.scroll_offset = self.cursor_y - visible_height + 1

        visible = lines[self.scroll_offset:self.scroll_offset + visible_height]

        for idx, line in enumerate(visible):
            stdscr.addstr(3 + idx, 2, line[:width - 4])

        curses.curs_set(1)
        stdscr.move(3 + self.cursor_y - self.scroll_offset, 2 + self.cursor_x)

    # ================= MAIN LOOP =================

    def run(self, stdscr):
        curses.curs_set(0)
        curses.start_color()
        stdscr.timeout(100)

        if not self.update_checked:
            self.remote_version = self.check_update()
            self.update_checked = True

            if self.remote_version:
                local = self.parse_version(self.VERSION)
                remote = self.parse_version(self.remote_version)

                if remote > local:
                    patch_diff = remote[2] - local[2]
                    if patch_diff > 9:
                        self.download_update()

        while True:
            stdscr.clear()

            if self.state == "menu":
                self.draw_menu(stdscr)
            elif self.state == "notes_menu":
                self.draw_notes_menu(stdscr)
            elif self.state == "note_editor":
                self.draw_note_editor(stdscr)

            if self.status_timer > 0:
                h, _ = stdscr.getmaxyx()
                stdscr.addstr(h - 2, 1, self.status_message)
                self.status_timer -= 1

            stdscr.refresh()
            key = stdscr.getch()

            # Update manual
            if key in (ord('u'), ord('U')) and self.remote_version:
                local = self.parse_version(self.VERSION)
                remote = self.parse_version(self.remote_version)
                if remote > local:
                    self.download_update()

            if self.state == "menu":
                if key == curses.KEY_UP and self.current_selection > 0:
                    self.current_selection -= 1
                elif key == curses.KEY_DOWN and self.current_selection < len(self.menu_items)-1:
                    self.current_selection += 1
                elif key == 10:
                    choice = self.menu_items[self.current_selection]
                    if choice == "Notes":
                        self.state = "notes_menu"
                    elif choice == "Exit":
                        return

            elif self.state == "notes_menu":
                names = list(self.notes.keys())

                if key == 27:
                    self.state = "menu"

                elif key == curses.KEY_UP and self.notes_selection > 0:
                    self.notes_selection -= 1

                elif key == curses.KEY_DOWN and self.notes_selection < len(names)-1:
                    self.notes_selection += 1

                elif key == 10 and names:
                    self.current_note_name = names[self.notes_selection]
                    self.current_note_content = self.notes[self.current_note_name]
                    self.cursor_x = self.cursor_y = 0
                    self.state = "note_editor"

                elif key in (ord('n'), ord('N')):
                    name = f"Note_{len(self.notes)+1}"
                    self.notes[name] = ""
                    self.notes_selection = len(self.notes)-1
                    self.current_note_name = name
                    self.current_note_content = ""
                    self.state = "note_editor"

            elif self.state == "note_editor":
                lines = self.current_note_content.split("\n")

                if key == 27:
                    self.notes[self.current_note_name] = self.current_note_content
                    self.save_notes()
                    curses.curs_set(0)
                    self.state = "notes_menu"

                elif key == 19:
                    self.notes[self.current_note_name] = self.current_note_content
                    self.save_notes()

                elif key in (curses.KEY_BACKSPACE, 127, 8):
                    if self.cursor_x > 0:
                        line = lines[self.cursor_y]
                        line = line[:self.cursor_x - 1] + line[self.cursor_x:]
                        lines[self.cursor_y] = line
                        self.cursor_x -= 1
                    self.current_note_content = "\n".join(lines)

                elif 32 <= key <= 126:
                    line = lines[self.cursor_y]
                    line = line[:self.cursor_x] + chr(key) + line[self.cursor_x:]
                    lines[self.cursor_y] = line
                    self.cursor_x += 1
                    self.current_note_content = "\n".join(lines)


def main():
    osys = PythOS()
    curses.wrapper(osys.run)


if __name__ == "__main__":
    main()
