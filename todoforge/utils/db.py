from todoforge.utils.config import todo_config
from todoforge.utils.constants import (
    DEFAULT_TODO_FOLDER,
)


def get_todos() -> dict:
    curr_space = todo_config.get_current_space()
    todo_filename = f"{curr_space}_todo.json"
    return todo_config.get(filepath=DEFAULT_TODO_FOLDER / todo_filename)


def save_todos(todos: dict) -> None:
    curr_space = todo_config.get_current_space()
    todo_filename = f"{curr_space}_todo.json"
    todo_config.save(filepath=DEFAULT_TODO_FOLDER / todo_filename, content=todos)
