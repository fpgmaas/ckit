from __future__ import annotations

import os
import subprocess
from dataclasses import dataclass

import click


@dataclass
class Argument:
    name: str
    default: str = None


@dataclass
class Boolean:
    """
    Class to hold a boolean option, that will prompt the user for yes/no before executing the command.

    Args:
        name: Name of the boolean. Should match $name in the command.
        prompt: The prompt to show to the user.
        if_true: Value that will replace $name if user chooses `Y`.
        if_true: Value that will replace $name if user chooses `N`. Defaults to "".
        default: Default value (True/False corresponding to `Y`/`N`) if the user presses Enter instead of making a choice.
    """

    name: str
    prompt: str
    if_true: str
    if_false: str = ""
    default: bool = True


class Command:
    def __init__(
        self,
        name: str,
        cmd: str | list(str),
        echo: bool = True,
        args: list[str | dict[str, any]] = None,
        booleans: list[dict[str, any]] = None,
    ) -> None:
        """
        A command object.
        """
        self.name = name
        self.cmd = [cmd] if isinstance(cmd, str) else cmd
        self.echo = echo
        self.arguments = self._parse_arguments(args) if args else None
        self.booleans = self._parse_booleans(booleans) if booleans else None

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

    def _parse_booleans(self, booleans: list[dict[str, any]]) -> list[Argument]:
        """
        Parse a list of boolean definitions into Boolean objects.

        Args:
            args: A list of dictonaries, where the keys are the names of the Boolean object, and the values are dicts with key-value pairs for the other
            properties. Valid values for these key-value paris are the class attributes of the Boolean class, except for 'name'.
        """
        parsed_booleans = []
        for boolean in booleans:
            name = list(boolean.keys())[0]
            value = list(boolean.values())[0]
            parsed_booleans.append(Boolean(name=name, **value))
        return parsed_booleans

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

        if self.arguments or self.booleans:
            cmd = self._prompt_and_replace_arguments_and_booleans(cmd)

        for command in cmd:
            if self.echo:
                click.echo(command)
            proc = subprocess.run(self._expand_env_vars(command), shell=True)
            if proc.returncode:
                # Stop running commands if a command fails.
                break
        return proc

    @staticmethod
    def _expand_env_vars(command):
        """
        Replace environment variables with their values.
        """
        return os.path.expandvars(command)

    def _prompt_and_replace_arguments_and_booleans(self, cmd):
        """
        For each argument or boolean, prompt the user for input, and then replace the matching string in the cmd.
        """
        commands_formatted_to_print = "\n".join(cmd)
        click.echo(f"Command{'s' if len(cmd) > 1 else ''} to be run:\n\n{commands_formatted_to_print}\n")
        if self.arguments:
            cmd = self._prompt_and_replace_arguments(cmd)
        if self.booleans:
            cmd = self._prompt_and_replace_booleans(cmd)
        return cmd

    def _prompt_and_replace_arguments(self, cmd):
        """
        For each argument, prompt the user for input, and then replace the matching string in the cmd.
        """
        for argument in self.arguments:
            value = click.prompt(
                f"Please enter a value for argument `{argument.name}`", type=str, default=argument.default
            )
            cmd = [command.replace(f"${argument.name}", value) for command in cmd]
        return cmd

    def _prompt_and_replace_booleans(self, cmd):
        """
        For each boolean, prompt the user for input, and then replace the matching string in the cmd.
        """
        for boolean in self.booleans:
            value = click.confirm(f"{boolean.prompt}", default=boolean.default)
            replacement = boolean.if_true if value else boolean.if_false
            cmd = [command.replace(f"${boolean.name}", replacement) for command in cmd]

        return cmd

    def __repr__(self):
        return f"Command `{self.name}`"

    def __str__(self):
        return f"Command {self.name} ---"
