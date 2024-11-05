# type: ignore
from textwrap import shorten

import typer
from rich import box, print
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from typing_extensions import Annotated

from todoforge.commands import spaces
from todoforge.utils.config import todo_config
from todoforge.utils.db import (
    get_todos,
    save_todos,
)
from todoforge.utils.helper import (
    edit_task_title_from_todo,
    handle_toggle_space_key,
    remove_task_from_todo,
    update_todo_status,
)
from todoforge.utils.models import TodoModel
from todoforge.utils.ui.menu import show_options

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

    current_space = todo_config.get_current_space()
    if current_space == "":
        print(
            "Oops... Looks like there is no space available. Please create a new space using [italic][green]tdf spaces add <name>[/green][/italic] and then try again."
        )
        raise typer.Exit(code=1)
    todos = get_todos()
    if len(todos["todos"]) == 0:
        print(
            "mmm... looks like you have no tasks at the moment. Create some new ones using [italic][green]tdf add <task>[/green][/italic]"
        )
        raise typer.Exit(code=1)

    console = Console()
    table = Table(title=f"{current_space.capitalize()}'s Todo List", box=box.MARKDOWN)

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
def toggle():
    """Toggle Task in an interactive window."""
    todos = get_todos()
    current_space = todo_config.get_current_space()
    updated_todos = show_options(
        title=f"{current_space.capitalize()}'s Todo List",
        items=todos["todos"],
        callback=handle_toggle_space_key,
    )

    save_todos({"todos": updated_todos})


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
    update_todo_status(todo_id=todo_id, status=True)


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
    update_todo_status(todo_id=todo_id, status=False)


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
