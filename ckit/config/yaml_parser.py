from __future__ import annotations

import json
import logging
from pathlib import Path

import yaml
from yaml.loader import SafeLoader

from ckit.command import Command
from ckit.command_group import CommandGroup


class YamlParser:
    """
    Class to read command groups from a yaml file.
    """

    def __init__(self):
        pass

    def parse(self, file: Path) -> dict[str, CommandGroup]:
        with open(file, "rb") as f:
            logging.debug(f"Parsing file {str(file)}")
            command_groups_raw = yaml.load(f, Loader=SafeLoader)

        if not command_groups_raw:
            logging.debug("No commands found in.")
            return {}

        command_groups = {}
        for group_name, group_commands in command_groups_raw.items():
            logging.debug(f"Parsing group '{group_name}' with commands: {json.dumps(group_commands, indent = 4)}")
            command_groups[group_name] = CommandGroup(
                commands={name: Command(name, **command_dict) for name, command_dict in group_commands.items()}
            )

        return command_groups
