from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from todoforge.schema import Base
from todoforge.utils.constants import DEFAULT_TODO_FOLDER


def get_db_url() -> str:
    db_path = DEFAULT_TODO_FOLDER / "todoforge.db"
    return f"sqlite:///{db_path}"


engine = create_engine(get_db_url(), echo=False)
SessionFactory = sessionmaker(bind=engine)

Base.metadata.create_all(engine)


@contextmanager
def db_session():
    session = SessionFactory()
    try:
        yield session
        session.commit()

    except SQLAlchemyError as sql_error:
        session.rollback()
        print(f"Database Error: {sql_error}")

    finally:
        session.close()
