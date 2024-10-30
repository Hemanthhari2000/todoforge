import json
from pathlib import Path
from typing import List

from todoforge.utils.constants import (
    DEFAULT_TODO_CONFIG,
)


class TodoConfig:
    def __init__(self) -> None:
        self._cached_config = {}

    def get_space_config(self):
        return self._load_config(filepath=DEFAULT_TODO_CONFIG)

    def get_current_space(self) -> str:
        return self._get_value_from_config("current_space")

    def get_spaces_list(self) -> List:
        return self._get_value_from_config("spaces")

    def get(self, filepath: Path) -> List:
        return self._load_config(filepath=filepath)

    def save(self, filepath: Path, content: dict) -> None:
        self._save_config(filepath=filepath, content=content)
        self._cached_config[str(filepath)] = content

    def _load_config(self, filepath: Path) -> dict:
        print(self._cached_config)
        print(filepath)
        if not self._cached_config or self._cached_config[str(filepath)]:
            with open(filepath, "r") as f:
                self._cached_config[str(filepath)] = json.load(f)
        return self._cached_config[str(filepath)]

    def _save_config(self, filepath: Path, content: dict) -> None:
        with open(filepath, "w") as f:
            json.dump(content, f, sort_keys=True, indent=4)

    def _get_value_from_config(self, field: str) -> str | List:
        space_config = self.get_space_config()
        value = space_config.get(field, None)
        if value is None:
            raise Exception(f"Field '{field}' in config file cannot be empty")
        return value


todo_config = TodoConfig()
