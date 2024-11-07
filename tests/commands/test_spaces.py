from pathlib import Path
from unittest.mock import patch

import pytest
from typer.testing import CliRunner

from todoforge.commands.spaces import app
from todoforge.utils.config import todo_config

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
        yield mock_get_current_space, mock_get_spaces_list, mock_save


@pytest.fixture
def mock_default_todo_folder():
    with patch(
        "todoforge.commands.spaces.DEFAULT_TODO_FOLDER",
        new=Path("/tmp/todoforge_folder"),
    ) as mock_folder:
        yield mock_folder


def test_add_space_command_where_todo_folder_does_not_exists(
    mock_todo_config, mock_default_todo_folder
):
    with patch("pathlib.Path.mkdir") as mock_mkdir:
        mock_get_current_space, _, mock_save = mock_todo_config
        mock_get_current_space.return_value = "work"
        mock_save.return_value = None

        result = runner.invoke(app, ["add", "work"])

        assert result.exit_code == 0
        assert "Space work has been created successfully" in result.output
        mock_save.assert_called()
        mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)


def test_add_space_command_with_invalid_space_name(
    mock_todo_config, mock_default_todo_folder
):
    mock_get_current_space, _, mock_save = mock_todo_config
    mock_get_current_space.return_value = "work"
    mock_save.return_value = None

    result = runner.invoke(app, ["add", "?work"])

    assert result.exit_code == 1
    assert (
        "Value error, name must contain only letters and numbers, no special characters"
        in result.output
    )


def test_ls_spaces(mock_todo_config):
    mock_get_current_space, mock_get_space_list, _ = mock_todo_config
    mock_get_space_list.return_value = ["work", "personal"]
    mock_get_current_space.return_value = "personal"

    result = runner.invoke(app, ["ls"])

    assert result.exit_code == 0
    assert "* personal" in result.output
    assert "work" in result.output


@patch(
    "todoforge.commands.spaces.DEFAULT_TODO_CONFIG",
    new=Path("/tmp/todoforge_folder/default_config.json"),
)
def test_switch_space(mock_todo_config):
    mock_get_current_space, mock_get_space_list, mock_save = mock_todo_config
    mock_get_space_list.return_value = ["work", "personal"]
    mock_get_current_space.return_value = "personal"
    mock_save.return_value = None

    result = runner.invoke(app, ["switch", "work"])

    assert result.exit_code == 0
    assert "Switched to 'work' space" in result.output
    mock_save.assert_called_with(
        filepath=Path("/tmp/todoforge_folder/default_config.json"),
        content={"current_space": "work", "spaces": ["work", "personal"]},
    )


def test_switch_space_with_incorrect_space_name(mock_todo_config):
    mock_get_current_space, mock_get_space_list, mock_save = mock_todo_config
    mock_get_space_list.return_value = ["work", "personal"]
    mock_get_current_space.return_value = "personal"
    mock_save.return_value = None

    result = runner.invoke(app, ["switch", "other"])

    assert result.exit_code == 1
    assert (
        "😬 Oh no... 'other' space is not available. Please create it first"
        in result.output
    )


def test_rename_space(mock_todo_config, mock_default_todo_folder):
    with patch("pathlib.Path.rename") as mock_rename:
        mock_get_current_space, mock_get_space_list, mock_save = mock_todo_config
        mock_get_space_list.return_value = ["work", "personal"]
        mock_get_current_space.return_value = "personal"
        mock_save.return_value = None

        result = runner.invoke(app, ["rename", "personal", "home"])

        assert result.exit_code == 0
        assert "Space personal has been renamed to home" in result.output
        mock_rename.assert_called_once_with(
            Path("/tmp/todoforge_folder/home_todo.json")
        )
        mock_save.assert_called()


def test_remove_space(mock_todo_config, mock_default_todo_folder):
    with patch("pathlib.Path.unlink") as mock_unlink, patch(
        "pathlib.Path.exists"
    ) as mock_exists:
        mock_get_current_space, mock_get_space_list, mock_save = mock_todo_config
        mock_get_space_list.return_value = ["work", "personal"]
        mock_get_current_space.return_value = "personal"
        mock_save.return_value = None
        mock_exists.return_value = True

        result = runner.invoke(app, ["remove", "personal"], input="y\ny\n")

        assert result.exit_code == 0
        assert "Space 'personal' has been removed" in result.output
        mock_unlink.assert_called_once_with()
        mock_save.assert_called_once()


def test_remove_space_with_invalid_space_name(
    mock_todo_config, mock_default_todo_folder
):
    with patch("pathlib.Path.unlink") as mock_unlink, patch(
        "pathlib.Path.exists"
    ) as mock_exists:
        mock_get_current_space, mock_get_space_list, mock_save = mock_todo_config
        mock_get_space_list.return_value = ["work"]
        mock_get_current_space.return_value = "work"
        mock_save.return_value = None
        mock_exists.return_value = False

        result = runner.invoke(app, ["remove", "personal"], input="y\ny\n")

        assert result.exit_code == 1
        assert "Space 'personal_todo.json' does not exist." in result.output
        assert mock_unlink.call_count == 0
        assert mock_save.call_count == 0
