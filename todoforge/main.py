from textwrap import shorten

import typer
from rich import box, print
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from typing_extensions import Annotated

from todoforge import __app_name__
from todoforge.commands import spaces
from todoforge.utils.db import (
    get_todos,
    save_todos,
)
from todoforge.utils.helper import (
    edit_task_title_from_todo,
    remove_task_from_todo,
    update_done_status,
)
from todoforge.utils.models import TodoModel

app = typer.Typer(no_args_is_help=True)
app.add_typer(spaces.app, name="spaces", help="Manage spaces", add_help_option=True)


@app.command()
def ls(
    full_id: Annotated[
        bool,
        typer.Option("--full-id/--not-full-id", "-f", help="Show full id for the todo"),
    ] = False
):
    """Show todos in current space."""

    todos = get_todos()
    console = Console()
    table = Table(title="Todo List", box=box.MARKDOWN)

    table.add_column("Id", justify="left", style="grey50", no_wrap=True)
    table.add_column("Title", justify="left", style="light_sea_green")
    table.add_column("Done", justify="center", style="red")

    sorted_todos = sorted(todos["todos"], key=lambda todo: todo["done"])
    for todo in sorted_todos:
        id_ = (
            todo["id"] if full_id else shorten(text=todo["id"], width=7, placeholder="")
        )

        table.add_row(
            id_,
            todo["title"].strip(),
            "[green]✔[/green]" if todo["done"] else "✘",
        )

    console.print(table)

    if not sorted_todos:
        print(
            "mmm... looks like you have no tasks at the moment. C'mon now create some new ones :smirk:"
        )


@app.command()
def add(
    title: str,
    done: Annotated[
        bool, typer.Option("--done/--not-done", help="Is the todo completed?")
    ] = False,
):
    """Add task to todos list."""

    try:
        todo = TodoModel(
            id=TodoModel.generate_id(title=title),
            title=title,
            done=done,
        )
        todo_store = get_todos()
        todo_store["todos"].append(todo.model_dump())
        save_todos(todos=todo_store)

        print("Task added successfully")
    except Exception as e:
        print(f"[red]{e}[/red]")
        typer.Exit()


@app.command()
def done(
    todo_id: Annotated[
        str,
        typer.Argument(
            metavar="todo-id",
            show_default=False,
            help="Todo id. Supports both partial and full id",
        ),
    ]
):
    """Mark todo as done."""
    update_done_status(todo_id=todo_id, status=True)


@app.command()
def undo(
    todo_id: Annotated[
        str,
        typer.Argument(
            metavar="todo-id",
            show_default=False,
            help="Todo id. Supports both partial and full id",
        ),
    ]
):
    """Mark todo as undone."""
    update_done_status(todo_id=todo_id, status=False)


@app.command()
def edit(
    todo_id: Annotated[
        str,
        typer.Argument(
            metavar="todo-id",
            show_default=False,
            help="Todo id. Supports both partial and full id",
        ),
    ]
):
    """Edit todo title."""

    title = Prompt.ask("Edit todo title to")

    edit_task_title_from_todo(todo_id=todo_id, edited_title=title)


@app.command()
def remove(
    todo_id: Annotated[
        str,
        typer.Argument(
            metavar="todo-id",
            show_default=False,
            help="Todo id. Supports both partial and full id",
        ),
    ]
):
    """Remove a task from the todo list."""

    remove_task_from_todo(todo_id=todo_id)


if __name__ == "__main__":
    app()
