import json
from pathlib import Path
from typing import Any

from todoforge.utils.constants import (
    DEFAULT_TODO_CONFIG,
)


class TodoConfig:
    def __init__(self) -> None:
        self._cached_config: dict[str, dict] = {}

    def get_space_config(self) -> dict:
        return self._load_config(DEFAULT_TODO_CONFIG)

    def get_current_space(self) -> str:
        return self._get_value_from_config("current_space", expected_type=str)

    def get_spaces_list(self) -> list[str]:
        return self._get_value_from_config("spaces", expected_type=list)

    def get(self, filepath: Path) -> dict:
        return self._load_config(filepath)

    def save(self, filepath: Path, content: dict) -> None:
        self._write_to_file(filepath=filepath, content=content)
        self._cached_config[str(filepath)] = content

    def _load_config(self, filepath: Path) -> dict:
        filepath_str = str(filepath)
        if filepath_str not in self._cached_config:
            self._cached_config[filepath_str] = self._read_from_file(filepath)
        return self._cached_config.get(filepath_str)

    def _read_from_file(self, filepath: Path) -> dict:
        if not filepath.exists():
            raise FileNotFoundError(f"Configuration file '{filepath}' does not exists")

        try:
            with open(filepath, "r") as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON from '{filepath}': {e}")

    def _write_to_file(self, filepath: Path, content: dict) -> None:
        with open(filepath, "w") as f:
            json.dump(content, f, sort_keys=True, indent=4)

    def _get_value_from_config(
        self, field: str, expected_type: Any = None
    ) -> str | list[str]:
        space_config = self.get_space_config()
        value = space_config.get(field, None)
        if value is None:
            raise KeyError(f"Field '{field}' is missing in the config file.")
        if expected_type and not isinstance(value, expected_type):
            raise TypeError(
                f"Field '{field}' is expected to be of type {expected_type.__name__}, but got {type(value).__name__}."
            )
        return value


todo_config = TodoConfig()
