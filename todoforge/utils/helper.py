from rich import print

from todoforge.utils.config import todo_config
from todoforge.utils.constants import (
    DEFAULT_TODO_CONFIG,
    DEFAULT_TODO_FOLDER,
)
from todoforge.utils.db import get_todos


def init_folders():
    if not DEFAULT_TODO_FOLDER.exists():
        DEFAULT_TODO_FOLDER.mkdir(parents=True, exist_ok=True)
        spaces_object = {"current_space": "", "spaces": []}
        todo_config.save(filepath=DEFAULT_TODO_CONFIG, content=spaces_object)


def update_todo_status(todo_id: str, status: bool) -> None:
    updates = {"done": status}
    _update_todo(todo_id=todo_id, updates=updates)


def edit_task_title_from_todo(todo_id: str, edited_title: str) -> None:
    """Edit task title from given todo id."""
    updates = {"title": edited_title}
    _update_todo(todo_id=todo_id, updates=updates)


def remove_task_from_todo(todo_id: str) -> None:
    """Removes a task from given todo id."""

    todos = get_todos()
    current_space = todo_config.get_current_space()
    todo_filename = f"{current_space}_todo.json"

    filtered_todos = [todo for todo in todos["todos"] if todo_id not in todo["id"]]

    # Check if anything was removed
    if len(filtered_todos) == len(todos["todos"]):
        print(f"Id '[green]{todo_id}[/green]' not found.")
    else:
        todos["todos"] = filtered_todos
        todo_config.save(filepath=DEFAULT_TODO_FOLDER / todo_filename, content=todos)
        print(f"Todo with id '[green]{todo_id}[/green]' has been removed.")


def handle_toggle_space_key(todos, idx):
    item_to_toggle = todos[idx]
    todos[idx]["done"] = not item_to_toggle["done"]
    return todos


def _update_todo(todo_id: str, updates: dict) -> None:
    current_space = todo_config.get_current_space()
    todo_filename = f"{current_space}_todo.json"

    todos = get_todos()

    is_updated = False
    for todo in todos["todos"]:
        if todo["id"].startswith(todo_id):
            todo.update(updates)
            is_updated = True
            break

    if not is_updated:
        print("Cannot find todo in todos list. Please check your todo id once.")
        return
    todo_config.save(filepath=DEFAULT_TODO_FOLDER / todo_filename, content=todos)
    print("Todo task updated successfully.")
