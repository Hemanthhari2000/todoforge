from contextlib import contextmanager

from sqlalchemy.exc import SQLAlchemyError

from todoforge.db.config import SessionFactory


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
