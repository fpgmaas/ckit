import os
from pathlib import Path


def get_global_commands_dir() -> Path:
    home = Path(os.environ["SKATE_HOME"]) if "SKATE_HOME" in os.environ else Path.home()
    return home / "skate"
