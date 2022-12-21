from __future__ import annotations

import os
from pathlib import Path


def get_global_commands_dir() -> Path:
    """
    Get the directory that contains the global command .yaml files.
    """
    home = Path(os.environ["CKIT_HOME"]) if "CKIT_HOME" in os.environ else Path.home() / "ckit"
    return home
