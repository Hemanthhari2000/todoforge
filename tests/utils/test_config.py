import json
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from todoforge.utils.config import TodoConfig


@pytest.fixture
def todo_config():
    return TodoConfig()


def test_get_space_config(todo_config):
    with patch.object(
        todo_config, "_load_config", return_value={"current_space": "work"}
    ):
        config = todo_config.get_space_config()
        assert config == {"current_space": "work"}


def test_get_current_space_with_expected_type_as_str(todo_config):
    with patch.object(todo_config, "_get_value_from_config", return_value="work"):
        current_space = todo_config.get_current_space()
        assert current_space == "work"
        assert isinstance(current_space, str)


def test_get_current_space_with_expected_type_as_list(todo_config):
    with patch.object(
        todo_config, "_get_value_from_config", return_value=["work", "personal"]
    ):
        with pytest.raises(
            TypeError, match="current space is expected to be of type str, but got list"
        ):
            todo_config.get_current_space()


def test_get_spaces_list_with_expected_type_as_list(todo_config):
    with patch.object(
        todo_config, "_get_value_from_config", return_value=["work", "personal"]
    ):
        spaces_list = todo_config.get_spaces_list()
        assert spaces_list == ["work", "personal"]


def test_get_space_list_with_expected_type_as_str(todo_config):
    with patch.object(todo_config, "_get_value_from_config", return_value="work"):
        with pytest.raises(
            TypeError, match="spaces is expected to be of type list, but got str."
        ):
            todo_config.get_spaces_list()


def test_get(todo_config):
    mock_filepath = Path("test.json")
    with patch.object(todo_config, "_load_config", return_value={"todos": []}):
        data = todo_config.get(mock_filepath)
        assert len(data["todos"]) == 0


def test_save(todo_config):
    mock_filepath = Path("test_path.json")
    content = {"todos": [{"id": "123", "title": "Test Task"}]}
    with patch.object(todo_config, "_write_to_file") as mock_write_to_file:
        todo_config.save(mock_filepath, content)
        mock_write_to_file.assert_called_once_with(
            filepath=mock_filepath, content=content
        )


def test_load_config(todo_config):
    mock_filepath = Path("config.json")
    with patch.object(
        todo_config, "_read_from_file", return_value={"setting": "value"}
    ):
        config = todo_config._load_config(mock_filepath)
        assert config == {"setting": "value"}


def test_read_from_file_with_valid_json_file(todo_config):
    with tempfile.NamedTemporaryFile(delete=False, mode="w") as temp_file:
        json.dump({"todos": []}, temp_file)
        mock_filepath = Path(temp_file.name)

    data = todo_config._read_from_file(mock_filepath)
    assert data == {"todos": []}


def test_read_from_file_where_file_is_not_present(todo_config):
    non_existent_file = Path("file_does_not_exists.json")

    with pytest.raises(
        FileNotFoundError,
        match="Configuration file 'file_does_not_exists.json' does not exists",
    ):
        todo_config._read_from_file(non_existent_file)


def test_read_from_file_with_invalid_json_contents(todo_config):
    with tempfile.NamedTemporaryFile(delete=False, mode="w") as temp_file:
        temp_file.write("INVALID JSON CONTENT")
        mock_filepath = Path(temp_file.name)

    with pytest.raises(ValueError) as excinfo:
        todo_config._read_from_file(mock_filepath)

    assert "Failed to parse JSON from" in str(excinfo.value)


def test_write_to_file(todo_config):
    mock_filepath = Path("data.json")
    content = {"todos": []}
    with patch("builtins.open", MagicMock()) as mock_open:
        todo_config._write_to_file(mock_filepath, content)
        mock_open.assert_called_once_with(mock_filepath, "w")


def test_get_value_from_config_with_non_empty_configuration(todo_config):
    with patch.object(
        todo_config, "get_space_config", return_value={"current_space": "work"}
    ):
        value = todo_config._get_value_from_config("current_space", str)
        assert value == "work"


def test_get_value_from_config_with_empty_configuration(todo_config):
    with patch.object(
        todo_config, "get_space_config", return_value={"current_space": ""}
    ):
        value = todo_config._get_value_from_config("current_space", str)
        assert len(value) == 0


def test_get_value_from_config_with_none_configuration(todo_config):
    with patch.object(todo_config, "get_space_config", return_value={}):
        with pytest.raises(
            KeyError, match="Field 'current_space' is missing in the config file."
        ):
            todo_config._get_value_from_config("current_space", str)


def test_get_value_from_config_with_return_value_as_a_list(todo_config):
    with patch.object(
        todo_config, "get_space_config", return_value={"spaces": ["work", "personal"]}
    ):
        value = todo_config._get_value_from_config("spaces", list)
        assert isinstance(value, list)
        assert len(value) == 2


def test_get_value_from_config_with_return_value_as_a_list_but_expected_type_as_str(
    todo_config,
):
    with patch.object(
        todo_config, "get_space_config", return_value={"spaces": ["work", "personal"]}
    ):
        with pytest.raises(
            TypeError,
            match="Field 'spaces' is expected to be of type str, but got list",
        ):
            todo_config._get_value_from_config("spaces", str)
