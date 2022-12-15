from __future__ import annotations

from dataclasses import dataclass

from skate.command import Command


@dataclass
class CommandGroup:
    commands: dict[str, Command]

    def get_command_names(self):
        return self.commands.keys()

    def get_command(self, name: str):
        return self.commands[name]
