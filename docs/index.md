<p align="center">
  <h1>peaks</h1>
</p>

---

[![Release](https://img.shields.io/github/v/release/fpgmaas/peaks)](https://img.shields.io/github/v/release/fpgmaas/peaks)
[![Build status](https://img.shields.io/github/actions/workflow/status/fpgmaas/peaks/main.yml?branch=main)](https://github.com/fpgmaas/peaks/actions/workflows/main.yml?query=branch%3Amain)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/peaks)](https://pypi.org/project/peaks/)
[![codecov](https://codecov.io/gh/fpgmaas/peaks/branch/main/graph/badge.svg)](https://codecov.io/gh/fpgmaas/peaks)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/peaks)](https://pypistats.org/packages/peaks)
[![License](https://img.shields.io/github/license/fpgmaas/peaks)](https://img.shields.io/github/license/fpgmaas/peaks)

_peaks_ is a command line utility to help you organise and quickly run frequently used commands.

<p align="center">
<img src="peaks.gif"/>
</p>

## Quickstart

### Installation

_peaks_ can be installed by running

```shell
pip install peaks
```

To get started, run

```shell
peaks init
```

which will prompt to add a `peaks/peaks.yaml` file in the user's home directory for global commands, and/or a `peaks.yaml` file in the current directory for commands specific to the current project. 

To use _peaks_ to run any of the pre-configured commands, simply run

```
peaks
```

For details regarding the configuration files, see the [configuration](https://fpgmaas.github.io/peaks/configuration) section of the documentation.

---

Repository initiated with [fpgmaas/cookiecutter-poetry](https://github.com/fpgmaas/cookiecutter-poetry).
