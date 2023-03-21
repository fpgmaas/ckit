## Configuration

_ckit_ looks for configuration in the following two locations

- From a `ckit.yaml` file in the current directory
- From any `.yaml` file in the the global configuration directory, which is defaulted to `~/ckit`, but which can be overridden with the environment variable `CKIT_HOME`.

Each `.yaml` file can contain one or more command groups, each containg one or more commands or other groups

```yaml
group-1:
  subgroup-1:
    command-a:
      ...
    command-b:
      ...
  subgroup-2:
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

### echo (Optional)

A boolean flag. By default, commands are printed to the terminal before being run. This can be suppressed by passing `false` to this argument. Example:

```yaml
command:
  cmd: "echo Hello world!"
  echo: false
```

### args (Optional)

A list of arguments for the command. The user will be prompted for input before the command(s) specified in `cmd` will be run. The value of an argument named `name` will be made available as `$name` in the `cmd`. For example:

```yaml
command:
  cmd: "echo My name is $name"
  args:
    - name
```

Arguments can be given a default value as follows:

```yaml
command:
  cmd: "echo My name is $name"
  args:
    - name: "Calvin"
```

### booleans (Optional)

A list of boolean arguments for the command, where the value in the command will depend on a `Y/N` prompt before the command(s) specified in `cmd` will be run. The value of a boolean argument named `name` will replace `$name` in the `cmd`. For example:

```yaml
  command-with-boolean:
    cmd: "ls $detailed"
    booleans:
      - detailed:
          prompt: "Show details?"
          if_true: -lh
```

By default, the value that is passed when the user chooses `N` is `""`. This can be changed with the `if_false` argument. The default choice can be changed from `Y` to `N` with the `default` argument. See the following example:

```yaml
  command-with-boolean:
    cmd: "echo I like $fruit"
    echo: false
    booleans:
      - fruit:
          prompt: "Do you like apples (y) or pears (n)?"
          if_true: apples
          if_false: pears
          default: false
```