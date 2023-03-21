from ckit.command import Command
from ckit.config.config import Config
from ckit.group import Group


def test_config():
    commandgroup1 = Group(elements={"echo": Command(name="echo", cmd="echo Hello world!")})
    commandgroup2 = Group(elements={"echo2": Command(name="echo2", cmd="echo Hello world!")})
    config = Config(local_groups=Group({"group1": commandgroup1}), global_groups=Group({"group2": commandgroup2}))
    assert config.get_group_names() == {"local": ["group1"], "global": ["group2"]}
