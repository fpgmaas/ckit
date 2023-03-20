from __future__ import annotations

from dataclasses import dataclass

from ckit.command import Command


@dataclass
class CommandGroup:
    """
    Class to hold commands.
    """

    commands: dict[str, Command]

    def get_command_names(self) -> list[str]:
        return list(self.commands.keys())

    def get_command(self, name: str) -> Command:
        return self.commands[name]

    def __repr__(self):
        return f"CommandGroup with commands:`{list(self.commands.values())}`"

    def __str__(self):
        return f"CommandGroup with commands:`{list(self.commands.values())}`"
