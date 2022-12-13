from __future__ import annotations

import curses
from dataclasses import dataclass, field
from typing import Optional

from blessed import Terminal


@dataclass
class TerminalLine:
    text: str
    selectable: bool
    selected: bool = None

    def select(self):
        self.selected = True

    def deselect(self):
        self.selected = False


@dataclass
class Picker:
    """
    Select an option from a list of options. Example:

        Picker(["apple", "orange", "pear", "bear", "dog"], title= "Select a command.").pick()

    """

    options: list[str]
    title: Optional[str] = None
    lines: list[TerminalLine] = field(init=False, default=None)

    def __post_init__(self) -> None:
        # Create the terminal lines
        self.lines = []
        if self.title:
            self.lines += [TerminalLine(text, False) for text in self.title.split("\n") + [""]]
        for option in self.options:
            self.lines.append(TerminalLine(option, True, False))

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
        selectable_lines[selected_line_index].deselect()
        selectable_lines[to_be_selected_index].select()

    def select_next(self):
        """
        Select the next selectable line.
        """
        selectable_lines = [line for line in self.lines if line.selectable]
        selected_line_index = self.get_index_of_selected_from_selectable()
        to_be_selected_index = (selected_line_index + 1) % len(selectable_lines)
        selectable_lines[selected_line_index].deselect()
        selectable_lines[to_be_selected_index].select()

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

    def get_selected(self) -> tuple[str, str]:
        """
        Get the selected group and corresponding value.
        """
        index = self.get_index_of_selected_from_selectable()
        return self.options[index]

    def pick(self):
        term = Terminal()
        with term.fullscreen(), term.cbreak(), term.hidden_cursor():
            while True:
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
                            print(f"{term.clear_eol}> {term.orange}{line.text}{term.normal}")
                        else:
                            print(f"{term.clear_eol}  {line.text}")
                    else:
                        print(f"{term.clear_eol} {line.text}")

                # Listen for user input
                val = term.inkey()
                if val.code == curses.KEY_DOWN:
                    self.select_next()
                if val.code == curses.KEY_UP:
                    self.select_prev()
                if val.code == curses.KEY_ENTER:
                    return self.get_selected()


if __name__ == "__main__":
    k = Picker(["apple", "orange", "pear", "bear", "dog"], title="Select a command.").pick()
    print(k)
