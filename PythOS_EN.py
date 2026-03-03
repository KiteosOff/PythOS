import curses
import pickle
import os
import time
from datetime import datetime


class PythOS:

    VERSION = "1.2.8"

    def __init__(self):
        self.state = "menu"
        self.previous_state = ""
        self.current_selection = 0
        self.menu_items = ["Notes", "Timer", "Calculator", "Error Log", "About", "Exit"]

        self.notes = {}
        self.notes_selection = 0

        self.current_note_name = ""
        self.current_note_content = ""

        self.cursor_x = 0
        self.cursor_y = 0
        self.scroll_offset = 0

        self.rename_buffer = ""

        self.error_log = []
        self.current_error_message = ""

        self.status_message = ""
        self.status_timer = 0
        self.status_color = 4

        self.note_to_delete = None
        self.last_auto_save = time.time()

        self.load_notes()

        self.ERR_TEMPL = {
            "ERR-DT-CRRPTD": "{arg1} is corrupted.",
            "ERR-APP-INDVLPMT": "{arg1} is still in development.",
            "ERR-NAME-ALRDY-TKEN": "Name already taken.",
        }

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

    # ================= ERRORS =================

    def raiseERR(self, code, arg1=None):
        template = self.ERR_TEMPL.get(code, "Unknown error.")
        message = template.replace("{arg1}", str(arg1))

        timestamp = datetime.now().strftime("%H:%M:%S")
        self.error_log.append(f"[{timestamp}] {message}")

        if code == "ERR-DT-CRRPTD":
            self.current_error_message = message
            self.state = "error_popup"
        else:
            self.show_status(message, 4)

    def show_status(self, message, color_pair):
        self.status_message = message
        self.status_color = color_pair
        self.status_timer = 60

    # ================= DRAW =================

    def draw_menu(self, stdscr):
        stdscr.addstr(1, 2, f"PythOS {self.VERSION}", curses.A_BOLD)

        color_map = {
            "Notes": 1,
            "Timer": 2,
            "Calculator": 3,
            "Error Log": 7,
            "About": 5,
            "Exit": 6
        }

        for idx, item in enumerate(self.menu_items):
            color = curses.color_pair(color_map.get(item, 0))
            if idx == self.current_selection:
                stdscr.addstr(3 + idx, 4, item, color | curses.A_REVERSE)
            else:
                stdscr.addstr(3 + idx, 4, item, color)

    def draw_notes_menu(self, stdscr):
        stdscr.addstr(1, 2, "Notes", curses.color_pair(1) | curses.A_BOLD)
        stdscr.addstr(2, 2, "N=New  R=Rename  D=Delete  ENTER=Edit  ESC=Back")

        names = list(self.notes.keys())

        for idx, name in enumerate(names):
            if idx == self.notes_selection:
                stdscr.addstr(4 + idx, 4, name,
                              curses.color_pair(1) | curses.A_REVERSE)
            else:
                stdscr.addstr(4 + idx, 4, name,
                              curses.color_pair(1))

    def draw_note_editor(self, stdscr):
        height, width = stdscr.getmaxyx()

        stdscr.addstr(0, 0, f"Editing: {self.current_note_name}",
                      curses.color_pair(1) | curses.A_BOLD)
        stdscr.addstr(1, 0, "ESC=Save & Exit  CTRL+S=Save")

        lines = self.current_note_content.split("\n")
        visible_height = height - 4

        if self.cursor_y < self.scroll_offset:
            self.scroll_offset = self.cursor_y
        elif self.cursor_y >= self.scroll_offset + visible_height:
            self.scroll_offset = self.cursor_y - visible_height + 1

        visible_lines = lines[self.scroll_offset:self.scroll_offset + visible_height]

        for idx, line in enumerate(visible_lines):
            stdscr.addstr(3 + idx, 2, line[:width - 4], curses.color_pair(1))

        curses.curs_set(1)
        stdscr.move(3 + self.cursor_y - self.scroll_offset, 2 + self.cursor_x)

    def draw_error_log(self, stdscr):
        stdscr.addstr(1, 2, "Error Log", curses.color_pair(7) | curses.A_BOLD)
        stdscr.addstr(2, 2, "ESC = Back")

        for idx, entry in enumerate(self.error_log[-20:]):
            stdscr.addstr(4 + idx, 4, entry, curses.color_pair(7))

    def draw_confirm_delete(self, stdscr):
        stdscr.addstr(5, 5, f"Delete '{self.note_to_delete}' ?", curses.color_pair(4))
        stdscr.addstr(6, 5, "Y = Yes | N = No", curses.color_pair(4))

    def draw_confirm_exit(self, stdscr):
        stdscr.addstr(5, 5, "Exit PythOS ?", curses.color_pair(4))
        stdscr.addstr(6, 5, "Y = Yes | N = No", curses.color_pair(4))

    def draw_rename_input(self, stdscr):
        stdscr.addstr(5, 5, "Rename note:", curses.color_pair(1))
        stdscr.addstr(6, 5, self.rename_buffer, curses.color_pair(1))
        curses.curs_set(1)
        stdscr.move(6, 5 + len(self.rename_buffer))

    def draw_error_popup(self, stdscr):
        h, w = stdscr.getmaxyx()
        msg = self.current_error_message
        stdscr.attron(curses.color_pair(4))
        stdscr.addstr(h//2, (w-len(msg))//2, msg)
        stdscr.addstr(h//2 + 1, (w-18)//2, "Press any key...")
        stdscr.attroff(curses.color_pair(4))

    # ================= LOOP =================

    def run(self, stdscr):
        curses.curs_set(0)
        curses.start_color()

        curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        curses.init_pair(6, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(7, curses.COLOR_YELLOW, curses.COLOR_BLACK)

        stdscr.timeout(100)

        while True:
            stdscr.clear()

            if self.state == "menu":
                self.draw_menu(stdscr)
            elif self.state == "notes_menu":
                self.draw_notes_menu(stdscr)
            elif self.state == "note_editor":
                self.draw_note_editor(stdscr)
            elif self.state == "error_log":
                self.draw_error_log(stdscr)
            elif self.state == "confirm_delete":
                self.draw_confirm_delete(stdscr)
            elif self.state == "confirm_exit":
                self.draw_confirm_exit(stdscr)
            elif self.state == "rename_input":
                self.draw_rename_input(stdscr)
            elif self.state == "error_popup":
                self.draw_error_popup(stdscr)

            if self.status_timer > 0:
                h, _ = stdscr.getmaxyx()
                stdscr.addstr(h-2, 1, self.status_message,
                              curses.color_pair(self.status_color))
                self.status_timer -= 1

            stdscr.refresh()
            key = stdscr.getch()

            # AUTO SAVE
            if self.state == "note_editor":
                if time.time() - self.last_auto_save >= 30:
                    self.notes[self.current_note_name] = self.current_note_content
                    self.save_notes()
                    self.last_auto_save = time.time()
                    self.show_status("Auto-saved.", 1)

            # ================= STATES =================

            if self.state == "menu":
                if key == curses.KEY_UP and self.current_selection > 0:
                    self.current_selection -= 1
                elif key == curses.KEY_DOWN and self.current_selection < len(self.menu_items)-1:
                    self.current_selection += 1
                elif key == 10:
                    choice = self.menu_items[self.current_selection]

                    if choice == "Notes":
                        self.state = "notes_menu"
                    elif choice == "Error Log":
                        self.state = "error_log"
                    elif choice == "Exit":
                        self.state = "confirm_exit"
                    else:
                        self.raiseERR("ERR-APP-INDVLPMT", choice)

            elif self.state == "confirm_exit":
                if key in (ord('y'), ord('Y')):
                    return
                elif key in (ord('n'), ord('N')):
                    self.state = "menu"

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
                    self.cursor_x = self.cursor_y = 0
                    self.state = "note_editor"

                elif key in (ord('d'), ord('D')) and names:
                    self.note_to_delete = names[self.notes_selection]
                    self.state = "confirm_delete"

                elif key in (ord('r'), ord('R')) and names:
                    self.rename_buffer = names[self.notes_selection]
                    self.state = "rename_input"

            elif self.state == "rename_input":
                names = list(self.notes.keys())
                old = names[self.notes_selection]

                if key == 27:
                    self.state = "notes_menu"
                    curses.curs_set(0)

                elif key == 10:
                    new = self.rename_buffer.strip()
                    if not new:
                        self.raiseERR("ERR-DT-CRRPTD", "Empty name")
                    elif new in self.notes:
                        self.raiseERR("ERR-NAME-ALRDY-TKEN")
                    else:
                        self.notes[new] = self.notes.pop(old)
                        self.notes_selection = list(self.notes.keys()).index(new)
                        self.save_notes()
                        self.show_status("Note renamed.", 1)
                    self.state = "notes_menu"
                    curses.curs_set(0)

                elif key in (8, 127):
                    self.rename_buffer = self.rename_buffer[:-1]

                elif 32 <= key <= 126:
                    self.rename_buffer += chr(key)

            elif self.state == "confirm_delete":
                if key in (ord('y'), ord('Y')):
                    del self.notes[self.note_to_delete]
                    self.save_notes()
                    self.state = "notes_menu"
                    self.show_status("Note deleted.", 1)
                elif key in (ord('n'), ord('N')):
                    self.state = "notes_menu"

            elif self.state == "note_editor":
                lines = self.current_note_content.split("\n")

                if key == 27:
                    self.notes[self.current_note_name] = self.current_note_content
                    self.save_notes()
                    curses.curs_set(0)
                    self.state = "notes_menu"
                    self.show_status("Saved.", 1)

                elif key == 19:  # CTRL+S
                    self.notes[self.current_note_name] = self.current_note_content
                    self.save_notes()
                    self.show_status("Saved.", 1)

                elif key == 10:
                    line = lines[self.cursor_y]
                    new_line = line[self.cursor_x:]
                    lines[self.cursor_y] = line[:self.cursor_x]
                    lines.insert(self.cursor_y+1, new_line)
                    self.cursor_y += 1
                    self.cursor_x = 0
                    self.current_note_content = "\n".join(lines)

                elif 32 <= key <= 126:
                    line = lines[self.cursor_y]
                    line = line[:self.cursor_x] + chr(key) + line[self.cursor_x:]
                    lines[self.cursor_y] = line
                    self.cursor_x += 1
                    self.current_note_content = "\n".join(lines)

            elif self.state == "error_log":
                if key == 27:
                    self.state = "menu"

            elif self.state == "error_popup":
                self.state = "menu"


def main():
    osys = PythOS()
    curses.wrapper(osys.run)


if __name__ == "__main__":
    main()
