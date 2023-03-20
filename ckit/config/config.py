from __future__ import annotations

from dataclasses import dataclass

from ckit.group import Group


@dataclass
class Config:
    local_groups: Group
    global_groups: Group

    def get(self, local_or_global: str):
        if local_or_global == "local":
            return self.local_groups
        elif local_or_global == "global":
            return self.global_groups
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
        if self.local_groups:
            result["local"] = list(self.local_groups.get_group_names())
        if self.global_groups:
            result["global"] = list(self.global_groups.get_group_names())
        return result
