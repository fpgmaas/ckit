import os
from pathlib import Path


def get_global_commands_dir() -> Path:
    """
    Get the directory that contains the global command .yaml files.
    """
    home = Path(os.environ["peaks_HOME"]) if "peaks_HOME" in os.environ else Path.home() / "peaks"
    return home
