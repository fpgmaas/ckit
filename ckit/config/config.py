from __future__ import annotations

from dataclasses import dataclass

from ckit.command_group import CommandGroup


@dataclass
class Config:
    local_command_groups: dict[str, CommandGroup]
    global_command_groups: dict[str, CommandGroup]

    def get(self, local_or_global: str):
        if local_or_global == "local":
            return self.local_command_groups
        elif local_or_global == "global":
            return self.global_command_groups
        else:
            raise ValueError(f"local_or_global should be either 'local' or 'global', but found {local_or_global}")

    def get_command_group_names(self):
        """
        Return a dict with the command group names per local and global, e.g

        {
            "local" : ["docker", "git"],
            "global" : ["git", "python"]
        }
        """
        result = {}
        if self.local_command_groups:
            result["local"] = list(self.local_command_groups.keys())
        if self.global_command_groups:
            result["global"] = list(self.global_command_groups.keys())
        return result
