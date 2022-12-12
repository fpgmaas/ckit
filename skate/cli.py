from __future__ import annotations

import click

from skate.config.config_files_initiatior import ConfigFilesInitiator
from skate.core import Core


@click.group(invoke_without_command=True)
@click.pass_context
def skate(ctx) -> None:
    if not ctx.invoked_subcommand:
        Core().run()


@skate.command()
def init():
    ConfigFilesInitiator().init()
