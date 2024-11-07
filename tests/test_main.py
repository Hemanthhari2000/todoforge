from unittest.mock import patch

import pytest
from typer.testing import CliRunner

from todoforge.main import app, todo_config  # type: ignore[attr-defined]

runner = CliRunner()


@pytest.fixture
def mock_todo_config():
    with patch.object(
        todo_config, "get_current_space"
    ) as mock_get_current_space, patch.object(
        todo_config, "get_spaces_list"
    ) as mock_get_spaces_list, patch.object(
        todo_config, "save"
    ) as mock_save:
        mock_get_spaces_list.return_value = ["work, personal"]
        yield mock_get_current_space, mock_get_spaces_list, mock_save


@pytest.fixture
def mock_get_todos():
    todos_list = {
        "todos": [
            {"done": False, "id": "1234", "title": "Test Task #1"},
            {"done": True, "id": "2345", "title": "Test Task #2"},
        ]
    }

    with patch("todoforge.main.get_todos") as mock_get_todos:
        mock_get_todos.return_value = todos_list
        yield mock_get_todos


def test_ls_command_that_should_list_todos_in_current_space(
    mock_todo_config, mock_get_todos
):
    mock_get_current_space, _, _ = mock_todo_config
    mock_get_current_space.return_value = "work"

    result = runner.invoke(app, ["ls"])

    assert result.exit_code == 0
    assert "Test Task #1 |  ✘   |" in result.output
    assert "Test Task #2 |  ✔   |" in result.output


def test_ls_command_where_current_space_is_empty(mock_todo_config):

    mock_get_current_space, _, _ = mock_todo_config
    mock_get_current_space.return_value = ""

    result = runner.invoke(app, ["ls"])

    assert result.exit_code == 1
    assert (
        "Oops... Looks like there is no space available. Please create a new space"
        in result.output
    )


def test_ls_command_where_len_of_todos_is_zero(mock_todo_config, mock_get_todos):
    mock_get_current_space, _, _ = mock_todo_config
    mock_get_todo = mock_get_todos
    mock_get_current_space.return_value = "personal"
    mock_get_todo.return_value = {"todos": []}

    result = runner.invoke(app, ["ls"])

    assert result.exit_code == 1
    assert (
        "mmm... looks like you have no tasks at the moment. Create some new ones using"
        in result.output
    )


def test_add_command_that_should_add_todo_to_todo_list(mock_get_todos):

    new_todo_title = "New Task"
    with patch("todoforge.main.save_todos") as mock_save_todos:
        mock_save_todos.return_value = None

        result = runner.invoke(app, ["add", new_todo_title])

        assert result.exit_code == 0
        assert len(mock_get_todos.return_value["todos"]) == 3


def test_add_command_that_should_raise_an_exception(mock_get_todos):
    mock_get_todos.return_value = None

    result = runner.invoke(app, ["add", "new task"])

    assert "Oops... something went wrong!" in result.output


def test_toggle_command(mock_get_todos, mock_todo_config):
    mock_get_current_space, _, _ = mock_todo_config
    mock_get_current_space.return_value = "work"

    with patch("todoforge.main.show_options") as mock_show_options, patch(
        "todoforge.main.save_todos"
    ) as mock_save_todos:
        mock_show_options.return_value = {
            "id": "9876",
            "title": "Status Changed",
            "done": True,
        }

        mock_save_todos.return_value = None

        result = runner.invoke(app, ["toggle"])

        assert result.exit_code == 0
        mock_save_todos.assert_called_once_with(
            {"todos": {"id": "9876", "title": "Status Changed", "done": True}}
        )


def test_done_command_that_should_update_the_status_to_True():

    with patch("todoforge.main.update_todo_status") as mock_update_todo_status:
        mock_update_todo_status.return_value = None

        runner.invoke(app, ["done", "1234"])

        mock_update_todo_status.assert_called_once_with(todo_id="1234", status=True)


def test_undo_command_that_should_update_the_status_to_True():

    with patch("todoforge.main.update_todo_status") as mock_update_todo_status:
        mock_update_todo_status.return_value = None

        runner.invoke(app, ["undo", "1234"])

        mock_update_todo_status.assert_called_once_with(todo_id="1234", status=False)


def test_edit_command_that_should_edit_title_of_given_todo():
    new_title = "New Title"
    with patch(
        "todoforge.main.edit_task_title_from_todo"
    ) as mock_edit_task_title_from_todo:
        mock_edit_task_title_from_todo.return_value = None

        result = runner.invoke(app, ["edit", "1234"], input=new_title)

        assert result.exit_code == 0
        mock_edit_task_title_from_todo.assert_called_once_with(
            todo_id="1234", edited_title=new_title
        )


def test_remove_command_that_should_remove_task_from_todo_list():

    with patch("todoforge.main.remove_task_from_todo") as mock_remove_task_from_todo:
        mock_remove_task_from_todo.return_value = None

        result = runner.invoke(app, ["remove", "2345"])

        assert result.exit_code == 0
        mock_remove_task_from_todo.assert_called_once_with(todo_id="2345")
