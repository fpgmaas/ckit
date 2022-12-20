import os
from pathlib import Path


def get_global_commands_dir() -> Path:
    """
    Get the directory that contains the global command .yaml files.
    """
    home = Path(os.environ["ckit_HOME"]) if "ckit_HOME" in os.environ else Path.home() / "ckit"
    return home
