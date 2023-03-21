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
            all_command_group_names = self.config.get_group_names()

            # First time, we have to distinguish between local and global groups.
            local_or_global, command_group_name = GroupPicker(
                term, all_command_group_names, "Please choose a group."
            ).pick()
            group = self.config.get(local_or_global).get(command_group_name)

            # Now, keep picking a Group until a Command is found...
            command = None
            while not command:
                if group.contains_only_commands():
                    choice = Picker(term, group.get_names(), "Please choose a command.").pick()
                    command = group.get(choice)
                elif group.contains_only_groups():
                    choice = Picker(term, group.get_names(), "Please choose a group.").pick()
                    group = group.get(choice)
                else:
                    _, choice = GroupPicker(term, group.get_names_by_type(), "Please make a choice.").pick()
                    selected = group.get(choice)
                    if isinstance(selected, Group):
                        group = selected
                    else:
                        command = selected

        command.run()
