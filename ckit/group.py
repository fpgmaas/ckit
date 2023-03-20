from __future__ import annotations

from dataclasses import dataclass

from ckit.command import Command
from ckit.command_group import CommandGroup


@dataclass
class Group:
    """
    A Group object can hold either:
    - other Groups (That in turn hold other Groups or CommandGroups)
    - CommandGroups, that contain commands.
    """

    groups: dict[str, Group | CommandGroup] = None

    def __post_init__(self):
        if not self.groups:
            self.groups = {}

    def get_group_names(self) -> list[str]:
        return list(self.groups.keys())

    def get_group(self, name: str) -> Command:
        return self.groups[name]

    def add_group(self, name: str, group: Group | CommandGroup):
        self.groups[name] = group

    def join(self, group: Group):
        self.groups = {**self.groups, **group.groups}

    def __repr__(self):
        return "{" + "\n".join("{!r}: {!r},".format(k, v) for k, v in self.groups.items()) + "}"

    def __str__(self):
        return "{" + "\n".join("{!r}: {!r},".format(k, v) for k, v in self.groups.items()) + "}"
