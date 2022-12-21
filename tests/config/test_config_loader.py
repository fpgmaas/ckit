import os
from pathlib import Path

from ckit.config.config_loader import ConfigLoader
from ckit.utils import run_within_dir


def test_config_loader(tmp_path: Path) -> None:
    global_config = """
example:
  echo:
    cmd: "echo Hello World!"
"""

    local_config = """
example2:
  echo2:
    cmd: "echo Hello World!"
"""

    with run_within_dir(tmp_path):
        os.mkdir("ckit")
        os.environ["CKIT_HOME"] = str(tmp_path / "ckit")
        with open(tmp_path / "ckit" / "someconfig.yaml", "w") as f:
            f.write(global_config)
        with open(tmp_path / "ckit.yaml", "w") as f:
            f.write(local_config)

        config = ConfigLoader().load()
        local_command_groups = config.get("local")
        assert local_command_groups["example2"].get_command_names() == ["echo2"]

        global_command_groups = config.get("global")
        print(global_command_groups)
        assert global_command_groups["example"].get_command_names() == ["echo"]

        config = ConfigLoader(load_global=False).load()
        assert config.local_command_groups is not None
        assert config.global_command_groups is None

        config = ConfigLoader(load_local=False).load()
        assert config.local_command_groups is None
        assert config.global_command_groups is not None
