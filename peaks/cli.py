from __future__ import annotations

import click

from peaks.config.config_files_initiatior import ConfigFilesInitiator
from peaks.config.config_loader import ConfigLoader
from peaks.core import Core


@click.group(invoke_without_command=True)
@click.option(
    "--local-only",
    "-l",
    is_flag=True,
    help="Boolean flag to only select a command from local files.",
)
@click.option(
    "--global-only",
    "-g",
    is_flag=True,
    help="Boolean flag to only select a command from global files.",
)
@click.pass_context
def peaks(ctx, local_only: bool, global_only: bool) -> None:
    if not ctx.invoked_subcommand:
        if local_only and global_only:
            raise ValueError(
                """Command was run with '--global-only' and '--local-only'. Only one of them can be passed. If you want to load both local and global
            configuration files, simply omit the flags."""
            )
        config = ConfigLoader(load_local=not global_only, load_global=not local_only).load()
        Core(config).run()


@peaks.command()
def init():
    ConfigFilesInitiator().init()
