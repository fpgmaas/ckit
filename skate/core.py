from __future__ import annotations

from dataclasses import dataclass

from skate.config.config import Config
from skate.screens.group_picker import GroupPicker
from skate.screens.picker import Picker


@dataclass
class Core:
    config: Config

    def run(self):
        all_command_group_names = self.config.get_command_group_names()

        local_or_global, command_group_name = GroupPicker(
            all_command_group_names, "Please choose a command group."
        ).pick()

        command_group = self.config.get(local_or_global)[command_group_name]
        choice = Picker(list(command_group.get_command_names()), "Please choose a command.").pick()

        command_group.get_command(choice).run()
