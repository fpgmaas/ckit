from __future__ import annotations

from dataclasses import dataclass

from ckit.command import Command


@dataclass
class CommandGroup:
    commands: dict[str, Command]

    def get_command_names(self) -> list[str]:
        return list(self.commands.keys())

    def get_command(self, name: str) -> Command:
        return self.commands[name]
