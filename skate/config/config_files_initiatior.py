from dataclasses import dataclass
from pathlib import Path

import click

from skate.config.common import get_global_commands_dir

LOCAL_COMMANDS_YAML_DEFAULT = """example:
  echo:
    cmd: "echo Hello World!"

  command-without-echo:
    cmd: "echo Hello World!"
    echo: false

  command-with-env-var:
    cmd: "echo Current user is $USER"

  command-with-user-input:
    cmd: "echo Hello! My name is: $name. My favourite fruit is: $fruit"
    echo: false
    args:
      - name
      - fruit: apple

  one-long-command:
    cmd: "echo Lorem ipsum dolor sit amet,
    consectetur adipiscing elit,
    sed do eiusmod tempor incididunt"
    echo: false

  multiple-commands:
    cmd:
      - "echo Lorem ipsum dolor sit amet,"
      - "echo consectetur adipiscing elit"
    echo: false
"""

GLOBAL_COMMANDS_YAML_DEFAULT = """git:
  log:
    cmd: "git log --all --oneline --graph --decorate"
"""


@dataclass
class ConfigFilesInitiator:
    def init(self):
        """
        Check for the existence of local- and global configuration files, and if they do not exist,
        ask the user if they should be created.
        """
        self._init_global()
        self._init_local()

    def _init_local(self):
        """
        Check if a commands.yaml file exists in the current directory. Otherwise, ask the user
        if it needs to be created, and if so; created it.
        """
        if Path("commands.yaml").exists():
            click.echo("A local commands.yaml already exists.")
        else:
            if click.confirm("Create a commands.yaml file in the current directory?", default=True):
                with open("commands.yaml", "w") as f:
                    f.write(LOCAL_COMMANDS_YAML_DEFAULT)

    def _init_global(self):
        """
        Check if there is a global commands.yaml file. If it does not exist, ask the user if it should be created, and
        if so, create it.
        """
        global_commands_file = get_global_commands_dir() / "commands.yaml"
        if global_commands_file.exists():
            click.echo(f"{global_commands_file} already exists.")
        else:
            if click.confirm(f"Create a global commands.yaml file in {global_commands_file.parent}?", default=True):
                global_commands_file.parent.mkdir(parents=True, exist_ok=True)
                with open(global_commands_file, "w") as f:
                    f.write(GLOBAL_COMMANDS_YAML_DEFAULT)
