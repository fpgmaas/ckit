import curses
from dataclasses import dataclass, field
from typing import Any, Generic, List, Optional, Sequence, Tuple, TypeVar, Union


@dataclass
class Option:
    label: str
    value: Any


KEYS_ENTER = (curses.KEY_ENTER, ord("\n"), ord("\r"))
KEYS_UP = (curses.KEY_UP, ord("k"))
KEYS_DOWN = (curses.KEY_DOWN, ord("j"))
KEYS_SELECT = (curses.KEY_RIGHT, ord(" "))

OPTION_T = TypeVar("OPTION_T", str, Option)
PICK_RETURN_T = Tuple[OPTION_T, int]


@dataclass
class CommandPicker(Generic[OPTION_T]):
    """
    Modified from https://github.com/wong2/pick
    """

    options: Sequence[OPTION_T]
    title: Optional[str] = None
    indicator: str = "*"
    default_index: int = 0
    index: int = field(init=False, default=0)
    screen: Optional["curses._CursesWindow"] = None

    def move_up(self) -> None:
        self.index -= 1
        if self.index < 0:
            self.index = len(self.options) - 1

    def move_down(self) -> None:
        self.index += 1
        if self.index >= len(self.options):
            self.index = 0

    def get_selected(self) -> PICK_RETURN_T:
        """return the current selected option as a tuple: (option, index)
        or as a list of tuples (in case multiselect==True)
        """
        return self.options[self.index], self.index

    def get_title_lines(self) -> List[str]:
        if self.title:
            return self.title.split("\n") + [""]
        return []

    def get_option_lines(self) -> List[str]:
        lines: List[str] = []
        for index, option in enumerate(self.options):
            if index == self.index:
                prefix = self.indicator
            else:
                prefix = len(self.indicator) * " "

            option_as_str = option.label if isinstance(option, Option) else option
            lines.append(f"{prefix} {option_as_str}")

        return lines

    def get_lines(self) -> Tuple[List, int]:
        title_lines = self.get_title_lines()
        option_lines = self.get_option_lines()
        lines = title_lines + option_lines
        current_line = self.index + len(title_lines) + 1
        return lines, current_line

    def draw(self, screen: "curses._CursesWindow") -> None:
        """draw the curses ui on the screen, handle scroll if needed"""
        screen.clear()

        x, y = 1, 1  # start point
        max_y, max_x = screen.getmaxyx()
        max_rows = max_y - y  # the max rows we can draw

        lines, current_line = self.get_lines()

        # calculate how many lines we should scroll, relative to the top
        scroll_top = 0
        if current_line > max_rows:
            scroll_top = current_line - max_rows

        lines_to_draw = lines[scroll_top : scroll_top + max_rows]

        for line in lines_to_draw:
            screen.addnstr(y, x, line, max_x - 2)
            y += 1

        screen.refresh()

    def run_loop(self, screen: "curses._CursesWindow") -> Union[List[PICK_RETURN_T], PICK_RETURN_T]:
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
