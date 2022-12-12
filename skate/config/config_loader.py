from dataclasses import dataclass
from pathlib import Path

from skate.command_group_master import CommandGroupMaster
from skate.config.common import get_global_commands_file_path
from skate.config.yaml_parser import YamlParser


@dataclass
class ConfigLoader:
    def load(self) -> CommandGroupMaster:
        """
        Check for the existence of local- and global configuration files, and if they do not exist,
        ask the user if they should be created.
        """
        global_command_groups = self._load_global()
        local_command_groups = self._load_local()

        if not global_command_groups and not local_command_groups:
            return None

        return CommandGroupMaster(
            local_command_groups=local_command_groups, global_command_groups=global_command_groups
        )

    def _load_global(self):
        global_commands_file_path = get_global_commands_file_path()
        if global_commands_file_path.exists():
            return YamlParser().parse(global_commands_file_path)
        return {}

    def _load_local(self):
        if Path("commands.yaml").exists():
            return YamlParser().parse(Path("commands.yaml"))
        return {}
