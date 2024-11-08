from pathlib import Path
from unittest.mock import patch

import pytest

from todoforge.utils.constants import DEFAULT_TODO_FOLDER
from todoforge.utils.helper import (
    _update_todo,
    edit_task_title_from_todo,
    handle_toggle_space_key,
    remove_task_from_todo,
    update_todo_status,
)


@pytest.fixture
def mock_todo_data():
    return {
        "todos": [
            {"id": "1234", "title": "Sample Task", "done": False},
            {"id": "5678", "title": "Another Task", "done": False},
        ]
    }


@pytest.fixture
def mock_get_todos(mock_todo_data):
    with patch("todoforge.utils.helper.get_todos") as mock_get_todos:
        mock_get_todos.return_value = mock_todo_data
        yield mock_get_todos


@pytest.fixture
def mock_get_current_space():
    with patch(
        "todoforge.utils.config.todo_config.get_current_space"
    ) as mock_get_current_space:
        mock_get_current_space.return_value = "work"
        yield mock_get_current_space


@pytest.fixture
def mock_save():
    with patch("todoforge.utils.config.todo_config.save") as mock_save:
        mock_save.return_value = None
        yield mock_save


# Test update_todo_status
def test_update_todo_status_to_true(
    mock_todo_data, mock_get_todos, mock_get_current_space, mock_save
):
    update_todo_status("1234", True)

    assert mock_todo_data["todos"][0]["done"]
    mock_save.assert_called_once_with(
        filepath=Path(DEFAULT_TODO_FOLDER / "work_todo.json"),
        content=mock_todo_data,
    )


# Test update_todo_status
def test_update_todo_status_to_false(
    mock_todo_data, mock_get_todos, mock_get_current_space, mock_save
):
    update_todo_status("1234", True)
    update_todo_status("1234", False)

    assert not mock_todo_data["todos"][0]["done"]
    assert mock_save.call_count == 2
    mock_save.assert_called_with(
        filepath=Path(DEFAULT_TODO_FOLDER / "work_todo.json"),
        content=mock_todo_data,
    )


# Test edit_task_title_from_todo
def test_edit_task_title_from_todo(
    mock_todo_data, mock_get_todos, mock_get_current_space, mock_save
):
    original_todo_title = mock_todo_data["todos"][0]["title"]

    edit_task_title_from_todo("1234", "Updated Task")

    assert original_todo_title == "Sample Task"
    assert mock_todo_data["todos"][0]["title"] == "Updated Task"
    assert mock_save.call_count == 1
    mock_save.assert_called_once_with(
        filepath=Path(DEFAULT_TODO_FOLDER / "work_todo.json"),
        content=mock_todo_data,
    )


# Test remove_task_from_todo
def test_remove_task_from_todo(
    mock_todo_data, mock_get_todos, mock_get_current_space, mock_save
):
    remove_task_from_todo("1234")

    assert len(mock_todo_data["todos"]) == 1
    assert mock_todo_data["todos"][0]["id"] == "5678"
    assert mock_save.call_count == 1
    mock_save.assert_called_once_with(
        filepath=Path(DEFAULT_TODO_FOLDER / "work_todo.json"),
        content=mock_todo_data,
    )


def test_remove_task_from_todo_not_found(
    mock_todo_data, mock_get_todos, mock_get_current_space, mock_save, capsys
):
    remove_task_from_todo("9999")

    captured = capsys.readouterr()
    assert "Id '9999' not found." in captured.out
    mock_save.assert_not_called()


# Test handle_toggle_space_key
def test_handle_toggle_space_key():
    todos = [
        {"id": "1", "title": "Sample Task 1", "done": False},
        {"id": "2", "title": "Sample Task 2", "done": True},
    ]
    updated_todos = handle_toggle_space_key(todos, 0)
    assert updated_todos[0]["done"]

    updated_todos = handle_toggle_space_key(todos, 1)
    assert not updated_todos[1]["done"]


# Test _update_todo
def test_update_todo_found(
    mock_todo_data, mock_get_todos, mock_get_current_space, mock_save
):

    _update_todo("1234", {"title": "Updated Title", "done": True})

    assert mock_todo_data["todos"][0]["title"] == "Updated Title"
    assert mock_todo_data["todos"][0]["done"] is True
    mock_save.assert_called_once_with(
        filepath=Path(DEFAULT_TODO_FOLDER / "work_todo.json"),
        content=mock_todo_data,
    )


def test_update_todo_not_found(
    mock_todo_data, mock_get_todos, mock_get_current_space, mock_save, capsys
):
    _update_todo("9999", {"title": "Non-Existent Task", "done": True})

    captured = capsys.readouterr()
    assert (
        "Cannot find todo in todos list. Please check your todo id once."
        in captured.out
    )
    mock_save.assert_not_called()
