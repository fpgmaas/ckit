import os
from pathlib import Path
from unittest import mock

import yaml

from skate.config.config_files_initiatior import ConfigFilesInitiator
from skate.utils import run_within_dir


@mock.patch("click.confirm")
def test_config_files_initiator(mock_click, tmp_path: Path) -> None:
    mock_click.return_value = "y"

    with run_within_dir(tmp_path):
        os.environ["SKATE_HOME"] = str(tmp_path / "skate_home")
        ConfigFilesInitiator().init()

        assert "skate.yaml" in os.listdir()
        with open("skate.yaml", "rb") as f:
            command_groups_raw = yaml.load(f, Loader=yaml.loader.SafeLoader)
            assert "example" in command_groups_raw

        assert "skate.yaml" in os.listdir("skate_home")
        with open("skate_home/skate.yaml", "rb") as f:
            command_groups_raw = yaml.load(f, Loader=yaml.loader.SafeLoader)
            assert "example" in command_groups_raw
