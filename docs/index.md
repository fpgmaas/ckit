<p align="center">
  <h1>Skate</h1>
</p>

---

[![Release](https://img.shields.io/github/v/release/fpgmaas/skate)](https://img.shields.io/github/v/release/fpgmaas/skate)
[![Build status](https://img.shields.io/github/workflow/status/fpgmaas/skate/Main/main)](https://github.com/fpgmaas/skate/actions/workflows/main.yml?query=branch%3Amain)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/skate)](https://pypi.org/project/skate/)
[![codecov](https://codecov.io/gh/fpgmaas/skate/branch/main/graph/badge.svg)](https://codecov.io/gh/fpgmaas/skate)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/skate)](https://pypistats.org/packages/skate)
[![License](https://img.shields.io/github/license/fpgmaas/skate)](https://img.shields.io/github/license/fpgmaas/skate)

_skate_ is a command line utility to help you organise and quickly run frequently used commands.

<p align="center">
<img src="skate.gif"/>
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

For details regarding the configuration files, see the [configuration](https://fpgmaas.github.io/skate/configuration) section of the documentation.

---

Repository initiated with [fpgmaas/cookiecutter-poetry](https://github.com/fpgmaas/cookiecutter-poetry).
