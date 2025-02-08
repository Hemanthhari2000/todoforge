from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from todoforge.db.schema import Base
from todoforge.db.util import get_db_url

engine = create_engine(
    get_db_url(), echo=False, connect_args={"check_same_thread": False}
)
SessionFactory = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base.metadata.create_all(engine)
