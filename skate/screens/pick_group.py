import curses
from dataclasses import dataclass, field
from typing import List, Optional

KEYS_ENTER = (curses.KEY_ENTER, ord("\n"), ord("\r"))
KEYS_UP = (curses.KEY_UP, ord("k"))
KEYS_DOWN = (curses.KEY_DOWN, ord("j"))
KEYS_SELECT = (curses.KEY_RIGHT, ord(" "))


@dataclass
class TerminalLine:
    text: str
    selectable: bool
    selected: bool = None

    def get(self):
        if self.selectable:
            if self.selected:
                return f"> {self.text}"
            else:
                return f"  {self.text}"
        else:
            return self.text


@dataclass
class TerminalLines:
    lines: List[TerminalLine]

    def __post_init__(self) -> None:
        for line in self.lines:
            if line.selectable:
                line.selected = True
                break

    def get(self):
        """
        Return all lines
        """
        lines_to_return = []
        current_line = None
        for ix, line in enumerate(self.lines):
            lines_to_return.append(line.get())
            if line.selected:
                current_line = ix
        return lines_to_return, current_line

    def select_prev(self):
        """
        Select the previous selectable line.
        """
        selectable_lines = [line for line in self.lines if line.selectable]
        selected_line_index = self.get_index_of_selected()
        to_be_selected_index = (selected_line_index - 1) % len(selectable_lines)
        selectable_lines[selected_line_index].selected = False
        selectable_lines[to_be_selected_index].selected = True

    def select_next(self):
        """
        Select the next selectable line.
        """
        selectable_lines = [line for line in self.lines if line.selectable]
        selected_line_index = self.get_index_of_selected()
        to_be_selected_index = (selected_line_index + 1) % len(selectable_lines)
        selectable_lines[selected_line_index].selected = False
        selectable_lines[to_be_selected_index].selected = True

    def get_index_of_selected(self):
        """
        Get index of the currently selected line, relative to the selectable lines. i.e. the non-selectable lines are ignored.
        """
        selectable_lines = [line for line in self.lines if line.selectable]
        selected_line_index = [i for i, x in enumerate(selectable_lines) if x.selected][0]
        return selected_line_index


@dataclass
class GroupPicker:
    """
    Modified from https://github.com/wong2/pick
    """

    options: dict[str, list[str]]
    title: Optional[str] = None
    indicator: str = "*"
    default_index: int = 0
    index: int = field(init=False, default=0)
    screen: Optional["curses._CursesWindow"] = None
    lines: TerminalLines = field(init=False, default=None)

    def __post_init__(self) -> None:
        terminal_lines = []
        if self.title:
            terminal_lines += [TerminalLine(text, False) for text in self.title.split("\n") + [""]]
        for key, value in self.options.items():
            terminal_lines.append(TerminalLine(f"[{key}]", False))
            for name in value:
                terminal_lines.append(TerminalLine(name, True, False))
            terminal_lines.append(TerminalLine("", False))
        self.lines = TerminalLines(terminal_lines)

    def move_up(self) -> None:
        self.lines.select_prev()

    def move_down(self) -> None:
        self.lines.select_next()

    def get_selected(self) -> dict[str, str]:
        index = self.lines.get_index_of_selected()
        for group, elements in self.options.items():
            if index >= len(elements):
                index -= len(elements)
            else:
                return group, elements[index]

    def draw(self, screen: "curses._CursesWindow") -> None:
        """draw the curses ui on the screen, handle scroll if needed"""
        screen.clear()

        x, y = 1, 1  # start point
        max_y, max_x = screen.getmaxyx()
        max_rows = max_y - y  # the max rows we can draw

        lines, current_line = self.lines.get()

        # calculate how many lines we should scroll, relative to the top
        scroll_top = 0
        if current_line > max_rows:
            scroll_top = current_line - max_rows

        lines_to_draw = lines[scroll_top : scroll_top + max_rows]

        for line in lines_to_draw:
            screen.addnstr(y, x, line, max_x - 2)
            y += 1

        screen.refresh()

    def run_loop(self, screen: "curses._CursesWindow") -> tuple:
        while True:
            self.draw(screen)
            c = screen.getch()
            if c in KEYS_UP:
                self.move_up()
            elif c in KEYS_DOWN:
                self.move_down()
            elif c in KEYS_ENTER:
                return self.get_selected()

    def config_curses(self) -> None:
        try:
            # use the default colors of the terminal
            curses.use_default_colors()
            # hide the cursor
            curses.curs_set(0)
        except BaseException:
            # Curses failed to initialize color support, eg. when TERM=vt100
            curses.initscr()

    def _start(self, screen: "curses._CursesWindow"):
        self.config_curses()
        return self.run_loop(screen)

    def start(self):
        if self.screen:
            # Given an existing screen
            # don't make any lasting changes
            last_cur = curses.curs_set(0)
            ret = self.run_loop(self.screen)
            if last_cur:
                curses.curs_set(last_cur)
            return ret
        return curses.wrapper(self._start)
