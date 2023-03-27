<p align="center">
  <img alt="ckit logo" width="460" height="300" src="https://raw.githubusercontent.com/fpgmaas/ckit/main/docs/static/ckit-logo.svg">
</p>

---

[![Release](https://img.shields.io/github/v/release/fpgmaas/ckit)](https://img.shields.io/github/v/release/fpgmaas/ckit)
[![Build status](https://img.shields.io/github/actions/workflow/status/fpgmaas/ckit/main.yml?branch=main)](https://github.com/fpgmaas/ckit/actions/workflows/main.yml?query=branch%3Amain)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/ckit)](https://pypi.org/project/ckit/)
[![codecov](https://codecov.io/gh/fpgmaas/ckit/branch/main/graph/badge.svg)](https://codecov.io/gh/fpgmaas/ckit)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/ckit)](https://pypistats.org/packages/ckit)
[![License](https://img.shields.io/github/license/fpgmaas/ckit)](https://img.shields.io/github/license/fpgmaas/ckit)

_ckit_ is a command line utility to help you organise and quickly run frequently used commands.

<p align="center">
<img src="static/ckit.gif"/>
</p>

---
<p align="center">
<a href="https://github.com/fpgmaas/ckit-files/">Example configuration files</a>
</p>

---
## Quickstart

### Installation

_ckit_ can be installed by running

```shell
pip install ckit
```

To get started, run

```shell
ckit init
```

which will prompt to add a `ckit/ckit.yaml` file in the user's home directory for global commands, and/or a `ckit.yaml` file in the current directory for commands specific to the current project.  Alternatively, run

```bash
ckit init --download-global-defaults
```

to get started with a richer set of examples in the global configuration directory, see [ckit-files](https://github.com/fpgmaas/ckit-files/).

To use _ckit_ to run any of the pre-configured commands, simply run

```
ckit
```

For details regarding the configuration files, see the [configuration](https://fpgmaas.github.io/ckit/configuration) section of the documentation.

## Examples

For a list of example configuration files, see [ckit-files](https://github.com/fpgmaas/ckit-files).

---

Repository initiated with [fpgmaas/cookiecutter-poetry](https://github.com/fpgmaas/cookiecutter-poetry).
