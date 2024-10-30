from todoforge.utils.config import todo_config
from todoforge.utils.constants import (
    DEFAULT_TODO_FOLDER,
)
from todoforge.utils.db import get_todos


def update_todo_status(todo_id: str, status: bool = None) -> None:
    todos = get_todos()
    current_space = todo_config.get_current_space()
    todo_filename = f"{current_space}_todo.json"

    matching_todo = next(
        (todo for todo in todos["todos"] if todo_id in todo["id"]), None
    )

    if not matching_todo:
        print(f"Id {todo_id} not found.")
        return
    matching_todo["done"] = status if status else not matching_todo["done"]
    todo_config.save(filepath=DEFAULT_TODO_FOLDER / todo_filename, content=todos)
    print("Updated.")


def edit_task_title_from_todo(todo_id: str, edited_title: str) -> None:
    """Edit task title from given todo id."""

    todos = get_todos()
    current_space = todo_config.get_current_space()
    todo_filename = f"{current_space}_todo.json"

    matching_todo = next(
        (todo for todo in todos["todos"] if todo_id in todo["id"]), None
    )

    if matching_todo:
        matching_todo["title"] = edited_title
        todo_config.save(filepath=DEFAULT_TODO_FOLDER / todo_filename, content=todos)
        print("Todo title edited.")
    else:
        print(f"Id {todo_id} not found.")


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

