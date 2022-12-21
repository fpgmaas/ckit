import os
from pathlib import Path

from ckit.config.common import get_global_commands_dir


def test_get_global_config_dir():
    os.environ["CKIT_HOME"] = "/some/dir"
    assert get_global_commands_dir() == Path("/some/dir")
