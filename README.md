<p align="center">
  <h1>Skate</h1>
</p>

---

[![Release](https://img.shields.io/github/v/release/fpgmaas/skate)](https://img.shields.io/github/v/release/fpgmaas/skate)
[![Build status](https://img.shields.io/github/actions/workflow/status/fpgmaas/skate/main.yml?branch=main)](https://github.com/fpgmaas/skate/actions/workflows/main.yml?query=branch%3Amain)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/skate)](https://pypi.org/project/skate/)
[![codecov](https://codecov.io/gh/fpgmaas/skate/branch/main/graph/badge.svg)](https://codecov.io/gh/fpgmaas/skate)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/skate)](https://pypistats.org/packages/skate)
[![License](https://img.shields.io/github/license/fpgmaas/skate)](https://img.shields.io/github/license/fpgmaas/skate)

_skate_ is a command line utility to help you organise and quickly run frequently used commands.

<p align="center">
<img src="docs/skate.gif"/>
</p>

## Quickstart

### Installation

_skate_ can be installed by running

```shell
pip install skate
```

To get started, run

```shell
skate init
```

which will prompt to add a `skate/skate.yaml` file in the user's home directory for global commands, and/or a `skate.yaml` file in the current directory for commands specific to the current project. 

To use _skate_ to run any of the pre-configured commands, simply run

```
skate
```

For more information, see the [documentation](https://fpgmaas.github.io/skate/).

## Configuration

_skate_ can look for configuration in the following two locations:

- In a `skate.yaml` file in the current directory
- In any `.yaml` file in the the global configuration directory, which is defaulted to `~/skate`, but which can be overridden with the environment variable `SKATE_HOME`.

An example `.yaml` file could look as follows:

```yaml
test:
  my-command:
    cmd: "echo Hello! My name is: $name. My favourite fruit is: $fruit"
    echo: false
    args:
      - name
      - fruit: apple
```

Which adds the command group `test` wth a single command called `my-command`. When `my-command` is selected to be run, _skate_ prompts the user for `name` and `fruit` before running the command specified in `cmd`, where `fruit` is defaulted to `apple` if the user does not give any input.

For more details, see the [configuration](https://fpgmaas.github.io/skate/configuration) section of the documentation.

---

Repository initiated with [fpgmaas/cookiecutter-poetry](https://github.com/fpgmaas/cookiecutter-poetry).
