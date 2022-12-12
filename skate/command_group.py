from __future__ import annotations

from skate.command import Command


class CommandGroup:
    def __init__(self, commands: dict[str, Command]) -> None:
        self.commands = commands

    def get_command_names(self):
        return self.commands.keys()

    def get_command(self, name: str):
        return self.commands[name]
