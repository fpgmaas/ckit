from __future__ import annotations

import urllib.request
from dataclasses import dataclass
from pathlib import Path

import click
import requests

from ckit.config.common import get_global_commands_dir

COMMANDS_YAML_DEFAULT = """example:
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

  command-with-boolean:
    cmd: "ls $detailed"
    echo: false
    booleans:
      - detailed:
          prompt: Show details?
          if_true: -lh

  one-long-command:
    cmd: "echo Lorem ipsum dolor sit amet,
    consectetur adipiscing elit,
    sed do eiusmod tempor incididunt"

  multiple-commands:
    cmd:
      - "echo Lorem ipsum dolor sit amet,"
      - "echo consectetur adipiscing elit"

example-groups:
  group1:
    hello:
      cmd: "echo Hello World from group 1!"
      echo: false
  group2:
    hello:
      cmd: "echo Hello World from group 2!"
      echo: false
  hello:
      cmd: "echo Hello World!"
      echo: false
"""


@dataclass
class ConfigFilesInitiator:
    """
    Args:
      download_global_defaults (bool): If False, simply prompt to create ckit.yaml in the global config directory. If True,
      prompt to download files from the ckit-files repository.
      skip_global: Skip initializing the global configuration directory.
      skip_local: Skip initializing the local configuration file.
    """

    download_global_defaults: bool = False
    skip_global: bool = False
    skip_local: bool = False

    def init(self):
        if not self.skip_global:
            if self.download_global_defaults:
                self._init_global_by_downloading_config_files()
            else:
                self._init_global()
        if not self.skip_local:
            self._init_local()

    def _init_local(self):
        """
        Check if a ckit.yaml file exists in the current directory. Otherwise, ask the user
        if it needs to be created, and if so; created it.
        """
        if Path("ckit.yaml").exists():
            click.echo("A local ckit.yaml already exists.")
        else:
            if click.confirm("Create a ckit.yaml file in the current directory?", default=True):
                with open("ckit.yaml", "w") as f:
                    f.write(COMMANDS_YAML_DEFAULT)

    def _init_global(self):
        """
        Check if there is a global ckit.yaml file. If it does not exist, ask the user if it should be created, and
        if so, create it.
        """
        global_commands_dir = get_global_commands_dir()
        global_commands_file = global_commands_dir / "ckit.yaml"
        if global_commands_file.exists():
            click.echo(f"{global_commands_file} already exists.")
        else:
            if click.confirm(f"Create a global ckit.yaml file in {global_commands_dir}?", default=True):
                global_commands_dir.mkdir(parents=True, exist_ok=True)
                with open(global_commands_file, "w") as f:
                    f.write(COMMANDS_YAML_DEFAULT)

    def _init_global_by_downloading_config_files(self):
        """
        Download config files from the `ckit-files` repository.
        """
        global_commands_dir = get_global_commands_dir()
        config_files = self._list_config_files_from_github()
        if click.confirm(
            f"Download the files {[file['name'] for file in config_files]} and place them in {global_commands_dir}?",
            default=True,
        ):
            global_commands_dir.mkdir(parents=True, exist_ok=True)
            for file in config_files:
                urllib.request.urlretrieve(file["url"], global_commands_dir / file["name"])

    def _list_config_files_from_github(self):
        url = "https://api.github.com/repos/fpgmaas/ckit-files/contents/config-files"
        response_json = requests.get(url).json()
        return [{"name": x["name"], "url": x["download_url"]} for x in response_json]
