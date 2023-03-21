from __future__ import annotations

import logging
from pathlib import Path

import yaml
from yaml.loader import SafeLoader

from ckit.command import Command
from ckit.group import Group


class YamlParser:
    """
    Class to read command groups from a yaml file.
    """

    def __init__(self):
        pass

    def parse(self, file: Path) -> dict[str, Group]:
        with open(file, "rb") as f:
            logging.debug(f"Parsing file {str(file)}")
            specification = yaml.load(f, Loader=SafeLoader)

        if not specification:
            logging.debug("No commands found in.")
            return {}

        return self._parse(specification)

    def _parse(self, specification: dict[str, any]):
        groups = Group()
        for name, element in specification.items():
            if self._is_command(element):
                groups.add(name, Command(name, **element))
            else:
                groups.add(name, self._parse(element))
        return groups

    @staticmethod
    def _is_command(specification: dict[str, any]):
        "Check if 'cmd' is in the specification"
        return "cmd" in specification
