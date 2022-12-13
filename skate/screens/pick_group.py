import curses
from dataclasses import dataclass, field
from typing import Optional

from blessed import Terminal

KEYS_ENTER = 1
KEYS_UP = 2
KEYS_DOWN = 238
KEYS_SELECT = 3


@dataclass
class TerminalLine:
    text: str
    selectable: bool
    selected: bool = None


@dataclass
class GroupPicker:
    """
    Modified from https://github.com/wong2/pick
    """

    options: dict[str, list[str]]
    title: Optional[str] = None
    index: int = field(init=False, default=0)
    lines: list[TerminalLine] = field(init=False, default=None)

    def __post_init__(self) -> None:
        # Create the terminal lines
        self.lines = []
        if self.title:
            self.lines += [TerminalLine(text, False) for text in self.title.split("\n") + [""]]
        for key, value in self.options.items():
            self.lines.append(TerminalLine(f"[{key}]", False))
            for name in value:
                self.lines.append(TerminalLine(name, True, False))
            self.lines.append(TerminalLine("", False))

        # Select the first selectable line.
        for line in self.lines:
            if line.selectable:
                line.selected = True
                break

    def select_prev(self):
        """
        Select the previous selectable line.
        """
        selectable_lines = [line for line in self.lines if line.selectable]
        selected_line_index = self.get_index_of_selected_from_selectable()
        to_be_selected_index = (selected_line_index - 1) % len(selectable_lines)
        selectable_lines[selected_line_index].selected = False
        selectable_lines[to_be_selected_index].selected = True

    def select_next(self):
        """
        Select the next selectable line.
        """
        selectable_lines = [line for line in self.lines if line.selectable]
        selected_line_index = self.get_index_of_selected_from_selectable()
        to_be_selected_index = (selected_line_index + 1) % len(selectable_lines)
        selectable_lines[selected_line_index].selected = False
        selectable_lines[to_be_selected_index].selected = True

    def get_index_of_selected_from_selectable(self):
        """
        Get index of the currently selected line, relative to the selectable lines. i.e. the non-selectable lines are ignored.
        """
        selectable_lines = [line for line in self.lines if line.selectable]
        selected_line_index = [i for i, x in enumerate(selectable_lines) if x.selected][0]
        return selected_line_index

    def get_index_of_selected(self):
        """
        Get index of the currently selected line, relative to ALL lines.
        """
        selected_line_index = [i for i, x in enumerate(self.lines) if x.selected][0]
        return selected_line_index

    def get_selected(self) -> dict[str, str]:
        index = self.get_index_of_selected_from_selectable()
        for group, elements in self.options.items():
            if index >= len(elements):
                index -= len(elements)
            else:
                return group, elements[index]

    def pick(self):
        term = Terminal()
        while True:
            with term.fullscreen(), term.cbreak(), term.hidden_cursor():
                # Start at 0,0
                print(term.home(), end="")

                # calculate how many lines we should scroll, relative to the top
                max_lines = term.height - 1
                index_selected = self.get_index_of_selected()
                scroll_top = 0
                if index_selected >= max_lines:
                    scroll_top = index_selected - max_lines + 1

                # Print the lines
                for line in self.lines[scroll_top : scroll_top + max_lines]:
                    if line.selectable:
                        if line.selected:
                            print(f"> {term.orange}{line.text}{term.normal}")
                        else:
                            print(f"  {line.text}")
                    else:
                        print(line.text)

                # Listen for user input
                val = term.inkey()
                if val.code == curses.KEY_DOWN:
                    self.select_next()
                if val.code == curses.KEY_UP:
                    self.select_prev()
                if val.code == curses.KEY_ENTER:
                    return self.get_selected()


if __name__ == "__main__":
    GroupPicker({"group": ["apple", "orange", "pear"], "other": ["dog", "bear"]}).pick()
