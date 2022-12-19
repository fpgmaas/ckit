import os
from pathlib import Path
from unittest import mock

import yaml

from peaks.config.config_files_initiatior import ConfigFilesInitiator
from peaks.utils import run_within_dir


@mock.patch("click.confirm")
def test_config_files_initiator(mock_click, tmp_path: Path) -> None:
    mock_click.return_value = "y"

    with run_within_dir(tmp_path):
        os.environ["peaks_HOME"] = str(tmp_path / "peaks_home")
        ConfigFilesInitiator().init()

        assert "peaks.yaml" in os.listdir()
        with open("peaks.yaml", "rb") as f:
            command_groups_raw = yaml.load(f, Loader=yaml.loader.SafeLoader)
            assert "example" in command_groups_raw

        assert "peaks.yaml" in os.listdir("peaks_home")
        with open("peaks_home/peaks.yaml", "rb") as f:
            command_groups_raw = yaml.load(f, Loader=yaml.loader.SafeLoader)
            assert "example" in command_groups_raw
