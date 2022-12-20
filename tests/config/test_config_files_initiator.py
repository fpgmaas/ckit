import os
from pathlib import Path
from unittest import mock

import yaml

from ckit.config.config_files_initiatior import ConfigFilesInitiator
from ckit.utils import run_within_dir


@mock.patch("click.confirm")
def test_config_files_initiator(mock_click, tmp_path: Path) -> None:
    mock_click.return_value = "y"

    with run_within_dir(tmp_path):
        os.environ["ckit_HOME"] = str(tmp_path / "ckit_home")
        ConfigFilesInitiator().init()

        assert "ckit.yaml" in os.listdir()
        with open("ckit.yaml", "rb") as f:
            command_groups_raw = yaml.load(f, Loader=yaml.loader.SafeLoader)
            assert "example" in command_groups_raw

        assert "ckit.yaml" in os.listdir("ckit_home")
        with open("ckit_home/ckit.yaml", "rb") as f:
            command_groups_raw = yaml.load(f, Loader=yaml.loader.SafeLoader)
            assert "example" in command_groups_raw
