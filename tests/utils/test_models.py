import pytest

from todoforge.utils.models import SpaceModel, TodoModel


def test_space_model_should_throw_value_error_for_invalid_name():

    with pytest.raises(
        ValueError,
        match="name must contain only letters and numbers, no special characters allowed.",
    ):
        SpaceModel(name="work!")


def test_todo_model_generated_id_should_have_a_fixed_length_of_():
    title = "Task"
    todo = TodoModel(
        id=TodoModel.generate_id(title=title),
        title=title,
        done=False,
    )

    assert len(todo.id) == 40
    assert todo.title == "Task"
    assert isinstance(todo, TodoModel)
