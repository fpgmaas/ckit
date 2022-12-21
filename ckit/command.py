from __future__ import annotations

import os
import shlex
import subprocess
from dataclasses import dataclass

import click


@dataclass
class Argument:
    name: str
    default: str = None


class Command:
    def __init__(
        self, name: str, cmd: str | list(str), echo: bool = True, args: list[str | dict[str, any]] = None
    ) -> None:
        """
        A command object.
        """
        self.name = name
        self.cmd = [cmd] if isinstance(cmd, str) else cmd
        self.echo = echo
        self.arguments = self._parse_arguments(args) if args else None

        if self.arguments:
            self._validate_arguments()

    def _parse_arguments(self, args: list[str | dict[str, any]]) -> list[Argument]:
        """
        Parse a list of argument definitions into Argument objects.

        Args:
            args: A list of either strings, or dictionaries. If the element is a string, it will be an argument without a default.
                If it is a dict, the key will be the name of the argument, and the corresponding value will be the default.
        """
        arguments = []
        for arg in args:
            if isinstance(arg, dict):
                arguments.append(Argument(name=list(arg.keys())[0], default=list(arg.values())[0]))
            elif isinstance(arg, str):
                arguments.append(Argument(name=arg))
            else:
                raise ValueError(f"Argument should be type dict or string, but found {type(arg)}: {arg}")
        return arguments

    def _validate_arguments(self):
        """
        Validate that the arguments are actually used in the commands.
        """
        for argument in self.arguments:
            if not any([f"${argument.name}" in command for command in self.cmd]):
                click.echo(
                    f"Argument '{argument.name}' defined for command {self.name}, but '${argument.name}' not found in"
                    " the defined command."
                )

    def run(self):
        cmd = self.cmd

        if self.arguments:
            cmd = self._prompt_and_replace_arguments(cmd)

        for command in cmd:
            if self.echo:
                click.echo(command)
            return subprocess.run(shlex.split(self._expand_env_vars(command)))

    @staticmethod
    def _expand_env_vars(command):
        """
        Replace environment variables with their values.
        """
        return os.path.expandvars(command)

    def _prompt_and_replace_arguments(self, cmd):
        """
        For each argument, prompt the user for input, and then replace the matching string in the cmd.
        """
        commands_formatted_to_print = "\n".join(self.cmd)
        click.echo(f"Command{'s' if len(self.cmd) > 1 else ''} to be run:\n\n{commands_formatted_to_print}\n")
        for argument in self.arguments:
            value = click.prompt(
                f"Please enter a value for argument `{argument.name}`", type=str, default=argument.default
            )
            cmd = [command.replace(f"${argument.name}", value) for command in cmd]
        return cmd
