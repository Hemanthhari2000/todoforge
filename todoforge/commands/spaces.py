import typer
from rich import print

from todoforge.utils.config import todo_config
from todoforge.utils.constants import (
    DEFAULT_TODO_CONFIG,
    DEFAULT_TODO_FOLDER,
)
from todoforge.utils.models import SpaceModel

app = typer.Typer()


@app.command()
def add(space_name: str):
    """
    Creates a new space for organizing todos.

    This command allows the user to create a new space when related todos can be stored.
    A Space can be a specific context like 'personal' or 'work' to help categorize tasks.

    Args:
        space_name (str): Name of the space you want to create

    Returns:
        None: Prints if the space is created successfully or not

    Example:
        $ todoforge spaces add personal
    """
    try:
        space_name = SpaceModel(name=space_name).name
        if not DEFAULT_TODO_FOLDER.exists():
            DEFAULT_TODO_FOLDER.mkdir(parents=True, exist_ok=True)

        space_todo_filename = f"{space_name}_todo.json"
        todo_content: dict = {
            "todos": [],
        }

        todo_config.save(
            filepath=DEFAULT_TODO_FOLDER / space_todo_filename, content=todo_content
        )

        total_spaces = [
            str(ts.stem).split("_")[0] for ts in DEFAULT_TODO_FOLDER.glob("*_todo.json")
        ]
        spaces_dict = {
            "current_space": (
                todo_config.get_current_space() if len(total_spaces) > 1 else space_name
            ),
            "spaces": total_spaces,
        }
        todo_config.save(filepath=DEFAULT_TODO_CONFIG, content=spaces_dict)

    except (ValueError, OSError) as e:
        print(f"[red]{e}[/red]")
        raise typer.Exit()

    print(f"Space [green]{space_name}[/green] has been created successfully")


@app.command()
def ls():
    """
    Lists all available spaces.

    This command displays the names of all the spaces created by the user.

    Returns:
        None: Confirms the list of available spaces with asterisk (*) that let's the user know about the current working space.

    Example:
        $ todoforge ls
            * personal
              work
    """
    spaces = todo_config.get_spaces_list()
    current_space = todo_config.get_current_space()
    for s in spaces:
        prefix = "[green]*[/green]" if s == current_space else " "
        print(f"{prefix} {s}")


@app.command()
def switch(space_name: str):
    """
    Switch between spaces.

    Allows the user to switch the current working space to another one.

    Args:
        space_name (str): The name of the space to switch to.

    Returns:
        None: Confirms the switch to the specific space.

    Example:
        $ todoforge switch work
            Switched to work space
    """
    spaces = todo_config.get_spaces_list()

    if space_name not in spaces:
        print(
            f":grimacing: Oh no... '[red]{space_name}[/red]' space is not available. Please create it first"
        )
        raise typer.Exit()

    todo_config.save(
        filepath=DEFAULT_TODO_CONFIG,
        content={
            "current_space": space_name,
            "spaces": spaces,
        },
    )
    print(f"Switched to '[green]{space_name}[/green]' space")


@app.command()
def rename(old_name: str, new_name: str):
    """
    Renames an existing space.

    Changes the name of a specified space to a new one.

    Args:
        old_name (str): The current name of the space
        new_name (str): The new name of the space

    Returns:
        None: Confirms the rename of the specified space.

    Example:
        $ todoforge rename personal home
            Space 'personal' has been renamed to 'home'
    """
    spaces = todo_config.get_spaces_list()
    current_space = todo_config.get_current_space()

    current_space = new_name if old_name == current_space else current_space
    idx = spaces.index(old_name)
    spaces[idx] = new_name

    todo_config.save(
        filepath=DEFAULT_TODO_CONFIG,
        content={"current_space": current_space, "spaces": spaces},
    )

    old_todo_filename = DEFAULT_TODO_FOLDER / f"{old_name}_todo.json"
    old_todo_filename.rename(DEFAULT_TODO_FOLDER / f"{new_name}_todo.json")

    print(
        f"Space [green]{old_name}[/green] has been renamed to [green]{new_name}[/green]"
    )


@app.command()
def remove(space_name: str):
    """
    Removes a space.

    Deletes the specified space and its associated todos.

    Args:
        space_name (str): The name of the space to remove.

    Returns:
        None: Confirms the removal of the specified space.

    Example:
        $ todoforge remove personal
            Space 'personal' has been removed.
    """
    current_space = todo_config.get_current_space()
    space_name = current_space if space_name == "." else space_name
    typer.confirm(f"Do you really want to delete {space_name}?", abort=True)
    typer.confirm(
        "Be adviced, this will delete all of your saved todos too. Do you still want to continue?",
        abort=True,
    )

    todo_filename = DEFAULT_TODO_FOLDER / f"{space_name}_todo.json"
    if not todo_filename.exists():
        print(f"Space '[green]{space_name}_todo.json[/green]' does not exist.")
        raise typer.Exit(code=1)

    todo_filename.unlink()
    print(f"Space '[green]{space_name}[/green]' has been removed.")
    spaces = todo_config.get_spaces_list()
    spaces.remove(space_name)

    if space_name == current_space:
        current_space = spaces[0] if len(spaces) > 0 else ""
    todo_config.save(
        filepath=DEFAULT_TODO_CONFIG,
        content={
            "current_space": current_space,
            "spaces": spaces,
        },
    )
