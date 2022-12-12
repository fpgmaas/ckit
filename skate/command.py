from __future__ import annotations

import os
import subprocess

import click


class Command:
    def __init__(self, name: str, cmd: str | list(str), print: bool = False, args: list[str] = None) -> None:
        self.name = name
        self.cmd = cmd
        self.print = print
        self.arguments = args

        if self.arguments:
            self._validate_arguments()

    def _validate_arguments(self):
        for argument in self.arguments:
            if f"${argument}" not in self.cmd:
                click.echo(
                    f"Argument '{argument}' defined for command {self.name}, but '${argument}' not found in the defined"
                    " command."
                )

    def run(self):
        cmd = self.cmd

        if self.arguments:
            cmd = self._prompt_and_replace_arguments(cmd)

        if self.print:
            click.echo(cmd)

        subprocess.run(self._expand_env_vars(cmd).split(" "))

    @staticmethod
    def _expand_env_vars(cmd):
        return os.path.expandvars(cmd)

    def _prompt_and_replace_arguments(self, cmd):
        """
        For each argument, prompt the user for input, and then replace the matching string in the cmd.
        """
        click.echo(f"Command to be run:\n\n{self.cmd}\n")
        for argument in self.arguments:
            value = click.prompt(f"Please enter a value for argument `{argument}`", type=str)
            cmd = cmd.replace(f"${argument}", value)
        return cmd
