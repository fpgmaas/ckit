from __future__ import annotations

import logging
from pathlib import Path

import yaml
from yaml.loader import SafeLoader

from ckit.command import Command
from ckit.command_group import CommandGroup
from ckit.group import Group


class YamlParser:
    """
    Class to read command groups from a yaml file.
    """

    def __init__(self):
        pass

    def parse(self, file: Path) -> dict[str, CommandGroup]:
        with open(file, "rb") as f:
            logging.debug(f"Parsing file {str(file)}")
            specification = yaml.load(f, Loader=SafeLoader)

        if not specification:
            logging.debug("No commands found in.")
            return {}

        return self._parse(specification)

    def _parse(self, specification: dict[str, any]):
        command_groups = Group()
        for group_name, group_elements in specification.items():
            if self._is_group_of_commands(group_elements):
                command_groups.add_group(group_name, self._parse_group_of_commands(group_elements))
            else:
                command_groups.add_group(group_name, self._parse(group_elements))
        return command_groups

    def _parse_group_of_commands(self, specification):
        return CommandGroup(
            commands={name: Command(name, **command_dict) for name, command_dict in specification.items()}
        )

    @staticmethod
    def _is_group_of_commands(specification: dict[str, any]):
        "Check if 'cmd' is a key in the first entry of this dict"
        return "cmd" in list(specification[next(iter(specification))].keys())
