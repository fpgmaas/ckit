from __future__ import annotations

from dataclasses import dataclass

import click

from skate.config.config_loader import ConfigLoader
from skate.screens.pick_command import CommandPicker
from skate.screens.pick_group import GroupPicker


@dataclass
class Core:
    def run(self):
        command_group_master = ConfigLoader().load()
        if not command_group_master:
            click.echo("No configuration files were found. Did you initialize the application with `skate init`?")
        else:
            all_command_group_names = command_group_master._get_command_group_names()

            local_or_global, command_group_name = GroupPicker(
                all_command_group_names, "Please choose a command group."
            ).pick()

            command_group = command_group_master.get(local_or_global)[command_group_name]
            choice, index = CommandPicker(list(command_group.get_command_names()), "Please choose a command.").start()

            command_group.get_command(choice).run()
