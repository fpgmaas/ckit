import os
from pathlib import Path


def get_global_commands_file_path() -> Path:
    home = Path(os.environ["skate_HOME"]) if "skate_HOME" in os.environ else Path.home()
    return home / "skate" / "commands.yaml"
