from __future__ import annotations

import logging
import os
from pathlib import Path


def get_global_commands_dir() -> Path:
    """
    Get the directory that contains the global command .yaml files.
    """
    home = Path(os.environ["CKIT_HOME"]) if "CKIT_HOME" in os.environ else Path.home() / "ckit"
    logging.debug(f"The global command directory to source .yaml files from is {home}")
    return home
