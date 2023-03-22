from ckit.command import Command
from ckit.group import Group


def test_group():
    command = Command(name="cmd1", cmd="echo Hello")
    group = Group(elements={"cmd1": command})
    assert len(group.elements) == 1
    assert isinstance(group.elements["cmd1"], Command)


def test_add_group():
    command1 = Command(name="cmd1", cmd="echo Hello1")
    group = Group(elements={"cmd1": command1})
    command2 = Command(name="cmd2", cmd="echo Hello2")
    group.add("cmd2", command2)
    assert len(group.elements) == 2
    assert group.elements["cmd1"].cmd == ["echo Hello1"]
    assert group.elements["cmd2"].cmd == ["echo Hello2"]


def test_join_groups():
    command1 = Command(name="cmd1", cmd="echo Hello1")
    group1 = Group(elements={"cmd1": command1})
    command2 = Command(name="cmd2", cmd="echo Hello2")
    group2 = Group(elements={"cmd2": command2})
    group1.join(group2)
    assert len(group1.elements) == 2
    assert group1.elements["cmd1"].cmd == ["echo Hello1"]
    assert group1.elements["cmd2"].cmd == ["echo Hello2"]


def test_checks():
    command1 = Command(name="cmd1", cmd="echo Hello1")
    group1 = Group(elements={"cmd1": command1})
    assert group1.contains_only_commands()
    assert not group1.contains_only_groups()

    command2 = Command(name="cmd2", cmd="echo Hello2")
    group2 = Group(elements={"cmd2": command2})

    group1.add("group2", group2)
    assert not group1.contains_only_commands()
    assert not group2.contains_only_groups()


def test_list_elements():
    command1 = Command(name="cmd1", cmd="echo Hello1")
    group1 = Group(elements={"cmd1": command1})

    command2 = Command(name="cmd2", cmd="echo Hello2")
    group2 = Group(elements={"cmd2": command2})

    group1.add("group2", group2)

    overview = group1.get_names_by_type()
    assert overview["groups"] == ["group2"]
    assert overview["commands"] == ["cmd1"]
