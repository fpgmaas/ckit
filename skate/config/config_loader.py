from dataclasses import dataclass
from pathlib import Path

import click

from skate.config.common import get_global_commands_dir
from skate.config.config import Config
from skate.config.yaml_parser import YamlParser


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
            click.echo("No configuration files were found. Did you initialize the application with `skate init`?")

        return Config(local_command_groups=local_command_groups, global_command_groups=global_command_groups)

    def _load_global(self):
        global_commands_dir = get_global_commands_dir()
        global_command_groups = {}
        if global_commands_dir.exists():
            yaml_files = list(global_commands_dir.glob("*.yaml"))
            if yaml_files:
                for yaml_file in yaml_files:
                    new_command_groups = YamlParser().parse(yaml_file)
                    global_command_groups = {**global_command_groups, **new_command_groups}
                return global_command_groups
        return {}

    def _load_local(self):
        if Path("commands.yaml").exists():
            return YamlParser().parse(Path("commands.yaml"))
        return {}
