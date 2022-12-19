import os
from pathlib import Path

from peaks.config.common import get_global_commands_dir


def test_get_global_config_dir():
    os.environ["peaks_HOME"] = "/some/dir"
    assert get_global_commands_dir() == Path("/some/dir")
