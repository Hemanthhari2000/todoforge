from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    pass


class Space(Base):
    __tablename__ = "spaces"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)
    todos = relationship("Todo", back_populates="space", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Space name={self.name}>"


class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    done = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    space_id = Column(Integer, ForeignKey("spaces.id"), nullable=False)
    space = relationship("Space", back_populates="todos")

    def __repr__(self) -> str:
        return f"<Todo title={self.title} done={self.done}>"
