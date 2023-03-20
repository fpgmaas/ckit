from unittest import mock

from ckit.command import Command


@mock.patch("click.prompt")
def test_command_with_argument(mock_prompt, capsys):
    mock_prompt.return_value = "Calvin"
    command = Command(name="test", cmd="echo Hello $name!", args=["name"])
    command.arguments[0].name = "name"
    command.arguments[0].default = None

    output = command.run()
    assert "echo Hello Calvin" in capsys.readouterr().out
    assert output.returncode == 0


def test_command_with_argument_with_default():
    command = Command(name="test", cmd="echo Hello $name!", args=[{"name": "Joe"}])
    command.arguments[0].name = "name"
    command.arguments[0].default = "Joe"


# Causes issue with tox in GH Action

# def test_command_stops_running_on_error(capsys):
#     command = Command(name="test", cmd=["echo123", "echo Hello"])
#     output = command.run()
#     assert "Hello" not in capsys.readouterr().out
#     assert output.returncode != 0
