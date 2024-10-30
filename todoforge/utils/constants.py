from pathlib import Path

DEFAULT_TODO_FOLDER = Path.home() / ".config" / "todoforge"
DEFAULT_TODO_FILENAME = Path.home().stem + "_todo.json"
DEFAULT_TODO_CONFIG = DEFAULT_TODO_FOLDER / "config.json"
