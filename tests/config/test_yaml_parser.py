from pathlib import Path

from ckit.config.yaml_parser import YamlParser
from ckit.utils import run_within_dir


def test_yaml_parser(tmp_path: Path) -> None:
    some_yaml = """
group1:
  echo:
    cmd: "echo Hello World!"
group2:
  echo:
    cmd: "echo Hello World!"
"""

    with run_within_dir(tmp_path):
        filepath = tmp_path / "somefile.yaml"
        with open(filepath, "w") as f:
            f.write(some_yaml)

        parsed_yaml = YamlParser().parse(filepath)
        assert parsed_yaml.get_group("group1").get_command_names() == ["echo"]
        assert parsed_yaml.get_group("group2").get_command_names() == ["echo"]
