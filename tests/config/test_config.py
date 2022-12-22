from ckit.command import Command
from ckit.command_group import CommandGroup
from ckit.config.config import Config


def test_config():
    commandgroup1 = CommandGroup(commands={"echo": Command(name="echo", cmd="echo Hello world!")})
    commandgroup2 = CommandGroup(commands={"echo2": Command(name="echo2", cmd="echo Hello world!")})
    config = Config(local_command_groups={"group1": commandgroup1}, global_command_groups={"group2": commandgroup2})
    assert config.get_command_group_names() == {"local": ["group1"], "global": ["group2"]}
