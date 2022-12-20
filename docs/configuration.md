## Configuration

_ckit_ looks for configuration in the following two locations

- From a `ckit.yaml` file in the current directory
- From any `.yaml` file in the the global configuration directory, which is defaulted to `~/ckit`, but which can be overridden with the environment variable `ckit_HOME`.

Each `.yaml` file can contain one or more command groups, each containg one or more commands

```yaml
group-1:
  command-1:
    ...
  command-2:
    ...
group-2:
  command-a:
    ...
  command-b:
    ...
```

## Command
A command has the following attributes:

### cmd

A string, or a list of strings, with the terminal command(s) to be run. Valid examples are:

```yaml
command:
  cmd: "echo Current user is $USER"
```

```yaml
command:
  cmd:
    - "echo Lorem ipsum dolor sit amet,"
    - "echo consectetur adipiscing elit"
```

### echo

A boolean flag. By default, commands are printed to the terminal before being run. This can be suppressed by passing `false` to this argument. Example:

```yaml
command:
  cmd: "echo Hello world!"
  echo: false
```

### args

A list of arguments for the command. The user will be prompted for input before the command(s) specified in `cmd` will be run. The value of an argument named `name` will be made available as `$name` in the `cmd`. For example:

```yaml
command:
  cmd: "echo My name is $name"
  args:
    - name
```

Arguments can be given a defalt value as follows:

```yaml
command:
  cmd: "echo My name is $name"
  args:
    - name: "Calvin"
```
