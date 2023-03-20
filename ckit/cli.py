from __future__ import annotations

import importlib.metadata as metadata
import logging

import click

from ckit.config.config_files_initiatior import ConfigFilesInitiator
from ckit.config.config_loader import ConfigLoader
from ckit.core import Core


def configure_logger(_ctx: click.Context, _param: click.Parameter, value: bool) -> None:
    log_level = logging.DEBUG if value else logging.INFO
    logging.basicConfig(level=log_level, handlers=[logging.StreamHandler()], format="%(message)s")


def display_version(ctx: click.Context, _param: click.Parameter, value: bool) -> None:
    if not value or ctx.resilient_parsing:
        return None

    click.echo(f'ckit {metadata.version("ckit")}')  # type: ignore[no-untyped-call]
    ctx.exit()


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
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help=(
        "Boolean flag for verbosity. Using this flag will display more information about files, imports and"
        " dependencies while running."
    ),
    expose_value=False,
    is_eager=True,
    callback=configure_logger,
)
@click.option(
    "--version",
    is_flag=True,
    is_eager=True,
    expose_value=False,
    callback=display_version,
    help="Display the current version and exit.",
)
@click.pass_context
def ckit(ctx, local_only: bool, global_only: bool) -> None:
    if not ctx.invoked_subcommand:
        if local_only and global_only:
            raise ValueError(
                """Command was run with '--global-only' and '--local-only'. Only one of them can be passed. If you want to load both local and global
            configuration files, simply omit the flags."""
            )
        config = ConfigLoader(load_local=not global_only, load_global=not local_only).load()
        Core(config).run()


@ckit.command()
def init():
    ConfigFilesInitiator().init()
