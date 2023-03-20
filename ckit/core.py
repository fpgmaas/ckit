from __future__ import annotations

from dataclasses import dataclass

from blessed import Terminal

from ckit.config.config import Config
from ckit.group import Group
from ckit.screens.group_picker import GroupPicker
from ckit.screens.picker import Picker


@dataclass
class Core:
    config: Config

    def run(self):
        term = Terminal()
        with term.fullscreen(), term.cbreak(), term.hidden_cursor():
            all_command_group_names = self.config.get_command_group_names()

            # First time, we have to distinguish between local and global groups.
            local_or_global, command_group_name = GroupPicker(
                term, all_command_group_names, "Please choose a group."
            ).pick()
            # Now, keep picking a Group until a CommandGroup is found...
            group = self.config.get(local_or_global).get_group(command_group_name)
            while isinstance(group, Group):
                choice = Picker(term, group.get_group_names(), "Please choose a group.").pick()
                group = group.get_group(choice)

            # ... then let the user pick a command.
            choice = Picker(term, group.get_command_names(), "Please choose a command.").pick()

        group.get_command(choice).run()
