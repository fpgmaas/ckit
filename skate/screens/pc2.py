from dataclasses import dataclass

from blessed import Terminal


@dataclass
class TerminalLine:
    text: str
    selectable: bool
    selected: bool = None



term = Terminal()
with term.fullscreen(), term.cbreak():
    print(term.home, end="")
    print(f"{term.green}Yellow is brown, {term.bright_yellow}Bright yellow is actually yellow!{term.normal}")
    while True:
        val = term.inkey()
        if val.code == 258:
            print(val.code)
