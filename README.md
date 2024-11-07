# `Todoforge`

Todoforge is a fast, custom-built CLI-based to-do tracker designed for productive developers. Organize tasks seamlessly by creating dedicated spaces (like work, personal, or project-specific), making task management more efficient and focused. Simple, intuitive, and lightweight, Todoforge enables you to boost productivity without the clutter of complex tools.

---

**Usage**:

```console
$ tdf [OPTIONS] COMMAND [ARGS]...
```

_NOTE: todoforge uses `tdf` alias for concise and better typing experience_

**Options**:

- `--install-completion`: Install completion for the current shell.
- `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
- `--help`: Show this message and exit.

**Commands**:

- `add`: Add task to todos list.
- `done`: Mark todo as done.
- `edit`: Edit todo title.
- `ls`: Show todos in current space.
- `remove`: Remove a task from the todo list.
- `spaces`: Manage spaces
- `toggle`: Toggle Task in an interactive window.
- `undo`: Mark todo as undone.

## `tdf add`

Add task to todos list.

**Usage**:

```console
$ tdf add [OPTIONS] TITLE
```

**Arguments**:

- `TITLE`: [required]

**Options**:

- `--done / --not-done`: Is the todo completed? [default: not-done]
- `--help`: Show this message and exit.

## `tdf done`

Mark todo as done.

**Usage**:

```console
$ tdf done [OPTIONS] todo-id
```

**Arguments**:

- `todo-id`: Todo id. Supports both partial and full id [required]

**Options**:

- `--help`: Show this message and exit.

## `tdf edit`

Edit todo title.

**Usage**:

```console
$ tdf edit [OPTIONS] todo-id
```

**Arguments**:

- `todo-id`: Todo id. Supports both partial and full id [required]

**Options**:

- `--help`: Show this message and exit.

## `tdf ls`

Show todos in current space.

**Usage**:

```console
$ tdf ls [OPTIONS]
```

**Options**:

- `-f, --full-id / --not-full-id`: Show full id for the todo [default: not-full-id]
- `--help`: Show this message and exit.

## `tdf remove`

Remove a task from the todo list.

**Usage**:

```console
$ tdf remove [OPTIONS] todo-id
```

**Arguments**:

- `todo-id`: Todo id. Supports both partial and full id [required]

**Options**:

- `--help`: Show this message and exit.

## `tdf spaces`

Manage spaces

**Usage**:

```console
$ tdf spaces [OPTIONS] COMMAND [ARGS]...
```

**Options**:

- `--help`: Show this message and exit.

**Commands**:

- `add`: Creates a new space for organizing todos.
- `ls`: Lists all available spaces.
- `remove`: Removes a space.
- `rename`: Renames an existing space.
- `switch`: Switch between spaces.

### `tdf spaces add`

Creates a new space for organizing todos.

This command allows the user to create a new space when related todos can be stored.
A Space can be a specific context like 'personal' or 'work' to help categorize tasks.

Args:
space_name (str): Name of the space you want to create

Returns:
None: Prints if the space is created successfully or not

Example:
$ todoforge spaces add personal

**Usage**:

```console
$ tdf spaces add [OPTIONS] SPACE_NAME
```

**Arguments**:

- `SPACE_NAME`: [required]

**Options**:

- `--help`: Show this message and exit.

### `tdf spaces ls`

Lists all available spaces.

This command displays the names of all the spaces created by the user.

Returns:
None: Confirms the list of available spaces with asterisk (\*) that let's the user know about the current working space.

Example:
$ todoforge ls \* personal
work

**Usage**:

```console
$ tdf spaces ls [OPTIONS]
```

**Options**:

- `--help`: Show this message and exit.

### `tdf spaces remove`

Removes a space.

Deletes the specified space and its associated todos.

Args:
space_name (str): The name of the space to remove.

Returns:
None: Confirms the removal of the specified space.

Example:
$ todoforge remove personal
Space 'personal' has been removed.

**Usage**:

```console
$ tdf spaces remove [OPTIONS] SPACE_NAME
```

**Arguments**:

- `SPACE_NAME`: [required]

**Options**:

- `--help`: Show this message and exit.

### `tdf spaces rename`

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

**Usage**:

```console
$ tdf spaces rename [OPTIONS] OLD_NAME NEW_NAME
```

**Arguments**:

- `OLD_NAME`: [required]
- `NEW_NAME`: [required]

**Options**:

- `--help`: Show this message and exit.

### `tdf spaces switch`

Switch between spaces.

Allows the user to switch the current working space to another one.

Args:
space_name (str): The name of the space to switch to.

Returns:
None: Confirms the switch to the specific space.

Example:
$ todoforge switch work
Switched to work space

**Usage**:

```console
$ tdf spaces switch [OPTIONS] SPACE_NAME
```

**Arguments**:

- `SPACE_NAME`: [required]

**Options**:

- `--help`: Show this message and exit.

## `tdf toggle`

Toggle Task in an interactive window.

**Usage**:

```console
$ tdf toggle [OPTIONS]
```

**Options**:

- `--help`: Show this message and exit.

## `tdf undo`

Mark todo as undone.

**Usage**:

```console
$ tdf undo [OPTIONS] todo-id
```

**Arguments**:

- `todo-id`: Todo id. Supports both partial and full id [required]

**Options**:

- `--help`: Show this message and exit.
