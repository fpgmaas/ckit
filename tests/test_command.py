from unittest import mock

from ckit.command import Command


@mock.patch("click.prompt")
def test_command_with_argument(mock_prompt, capsys):
    mock_prompt.return_value = "Calvin"
    command = Command(name="test", cmd="echo Hello $name!", args=["name"])
    assert command.arguments[0].name == "name"
    assert command.arguments[0].default is None

    output = command.run()
    assert "echo Hello Calvin" in capsys.readouterr().out
    assert output.returncode == 0


def test_command_with_argument_with_default():
    command = Command(name="test", cmd="echo Hello $name!", args=[{"name": "Joe"}])
    command.arguments[0].name = "name"
    command.arguments[0].default = "Joe"


@mock.patch("click.confirm")
def test_command_with_boolean_true(mock_confirm, capsys):
    mock_confirm.return_value = True
    boolean = {"message": {"prompt": "Print message?", "if_true": "Hello!"}}
    command = Command(name="test", cmd="echo $message", booleans=[boolean])
    assert command.booleans[0].name == "message"
    assert command.booleans[0].prompt == "Print message?"
    assert command.booleans[0].if_true == "Hello!"
    assert command.booleans[0].if_false == ""
    assert command.booleans[0].default

    output = command.run()
    assert "echo Hello!" in capsys.readouterr().out
    assert output.returncode == 0


@mock.patch("click.confirm")
def test_command_with_boolean_false(mock_confirm, capsys):
    mock_confirm.return_value = False
    boolean = {"message": {"prompt": "Print message?", "if_true": "Hello!", "if_false": "Hobbes"}}
    command = Command(name="test", cmd="echo $message", booleans=[boolean])
    assert command.booleans[0].name == "message"
    assert command.booleans[0].prompt == "Print message?"
    assert command.booleans[0].if_true == "Hello!"
    assert command.booleans[0].if_false == "Hobbes"
    assert command.booleans[0].default

    output = command.run()
    assert "echo Hobbes" in capsys.readouterr().out
    assert output.returncode == 0


# Causes issue with tox in GH Action

# def test_command_stops_running_on_error(capsys):
#     command = Command(name="test", cmd=["echo123", "echo Hello"])
#     output = command.run()
#     assert "Hello" not in capsys.readouterr().out
#     assert output.returncode != 0
