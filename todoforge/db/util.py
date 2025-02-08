from todoforge.utils.constants import DEFAULT_TODO_FOLDER


def get_db_url() -> str:
    db_path = DEFAULT_TODO_FOLDER / "todoforge.db"
    return f"sqlite:///{db_path}"
