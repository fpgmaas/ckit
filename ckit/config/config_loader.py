from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path

from ckit.config.common import get_global_commands_dir
from ckit.config.config import Config
from ckit.config.yaml_parser import YamlParser


@dataclass
class ConfigLoader:
    load_local: bool = True
    load_global: bool = True

    def load(self) -> Config:
        """
        Check for the existence of local- and global configuration files, and if they do not exist,
        ask the user if they should be created.
        """
        local_command_groups = self._load_local() if self.load_local else None
        global_command_groups = self._load_global() if self.load_global else None

        if not local_command_groups and not global_command_groups:
            exit("No configuration files were found. Did you initialize the application with `ckit init`?")

        return Config(local_command_groups=local_command_groups, global_command_groups=global_command_groups)

    def _load_global(self):
        """
        Find all .yaml files in the global commands directory, and extract the command groups and their commands.
        """
        logging.debug("Loading the global configuration files.")
        global_commands_dir = get_global_commands_dir()
        global_command_groups = {}
        if global_commands_dir.exists():
            yaml_files = []
            for extension in ["*.yaml", "*.yml"]:
                yaml_files.extend(global_commands_dir.glob(extension))
            logging.debug(f"Found the following global command files: {[str(file) for file in yaml_files]}")
            if yaml_files:
                for yaml_file in yaml_files:
                    new_command_groups = YamlParser().parse(yaml_file)
                    global_command_groups = {**global_command_groups, **new_command_groups}
                return global_command_groups
        return {}

    def _load_local(self):
        logging.debug("Loading the local configuration files.")
        if Path("ckit.yaml").exists():
            return YamlParser().parse(Path("ckit.yaml"))
        return {}
