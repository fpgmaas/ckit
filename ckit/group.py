from __future__ import annotations

from dataclasses import dataclass

from ckit.command import Command


@dataclass
class Group:
    """
    A Group object can hold either:
    - Other Groups (That in turn hold other Groups or Commands)
    - Commands
    """

    elements: dict[str, Group | Command] = None

    def __post_init__(self):
        if not self.elements:
            self.elements = {}

    def get_names(self) -> list[str]:
        return list(self.elements.keys())

    def get(self, name: str) -> Command:
        return self.elements[name]

    def add(self, name: str, element: Group):
        self.elements[name] = element

    def join(self, group: Group):
        self.elements = {**self.elements, **group.elements}

    def contains_only_commands(self):
        return all(isinstance(el, Command) for el in self.elements.values())

    def contains_only_groups(self):
        return all(isinstance(el, Group) for el in self.elements.values())

    def get_names_by_type(self):
        """
        Return a dict with keys 'groups' and 'commands', containing the names of the groups and commands
        respectively.
        """
        return {
            "groups": [k for k, v in self.elements.items() if isinstance(v, Group)],
            "commands": [k for k, v in self.elements.items() if isinstance(v, Command)],
        }

    def __repr__(self):
        return "{" + "\n".join("{!r}: {!r},".format(k, v) for k, v in self.elements.items()) + "}"

    def __str__(self):
        return "{" + "\n".join("{!r}: {!r},".format(k, v) for k, v in self.elements.items()) + "}"
