from unittest.mock import patch

import pytest

from todoforge.utils.config import todo_config
from todoforge.utils.constants import DEFAULT_TODO_FOLDER
from todoforge.utils.db import get_todos, save_todos


@pytest.fixture
def mock_todo_config():
    with patch.object(
        todo_config, "get_current_space"
    ) as mock_get_current_space, patch.object(
        todo_config, "get"
    ) as mock_get, patch.object(
        todo_config, "save"
    ) as mock_save:
        yield mock_get_current_space, mock_get, mock_save


def test_get_todos_when_the_todo_list_is_empty(mock_todo_config):
    mock_get_current_space, mock_get, _ = mock_todo_config
    mock_get_current_space.return_value = "work"
    mock_get.return_value = {"todos": []}

    todos = get_todos()

    assert len(todos["todos"]) == 0
    mock_get_current_space.assert_called_once()
    mock_get.assert_called_once()


def test_get_todos_when_the_todo_list_is_not_empty(mock_todo_config):
    mock_get_current_space, mock_get, _ = mock_todo_config
    mock_get_current_space.return_value = "work"
    mock_get.return_value = {
        "todos": [
            {"done": False, "id": "1234", "title": "Test Task #1"},
            {"done": True, "id": "2345", "title": "Test Task #2"},
        ]
    }

    todos = get_todos()

    assert len(todos["todos"]) == 2
    assert todos["todos"][0]["title"] == "Test Task #1"
    assert todos["todos"][1]["done"]
    mock_get_current_space.assert_called_once()
    mock_get.assert_called_once()


def test_save_todos_for_given_todos_dict(mock_todo_config):
    mock_get_current_space, _, mock_save = mock_todo_config
    mock_get_current_space.return_value = "work"
    mock_save.return_value = None
    todos_dict = {
        "todos": [
            {"done": False, "id": "1234", "title": "Test Task #1"},
            {"done": True, "id": "2345", "title": "Test Task #2"},
        ]
    }

    save_todos(todos=todos_dict)

    mock_get_current_space.assert_called_once()
    mock_save.assert_called_once_with(
        filepath=DEFAULT_TODO_FOLDER / "work_todo.json", content=todos_dict
    )
