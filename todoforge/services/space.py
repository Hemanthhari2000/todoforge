from todoforge.db.schema import AppState, Space
from todoforge.db.session import db_session
from todoforge.models import SpaceModel


class SpaceService:
    def add(self, space: SpaceModel) -> None:
        new_space = Space(**space.model_dump())
        with db_session() as session:
            session.add(new_space)
            session.flush()

            current_space = session.query(AppState).first()

            if current_space:
                current_space.current_space_id = new_space.id
            else:
                current_space = AppState(current_space_id=new_space.id)
                session.add(current_space)

    def get_all(self) -> tuple[list[SpaceModel], str] | None:
        with db_session() as session:
            spaces = session.query(Space).all()
            spaces = SpaceModel.from_db_model(spaces)

            current_space = session.query(AppState).first()
            if not current_space:
                return None
            return (spaces, current_space.current_space.name)

    def get_by_name(self, space_name: str) -> Space | None:
        with db_session() as session:
            return session.query(Space).filter(Space.name == space_name).first()

    def get_by_id(self, space_id: int) -> Space | None:
        with db_session() as session:
            return session.query(Space).filter(Space.id == space_id).first()

    def remove(self, space_name: str) -> None:
        space = self.get_by_name(space_name)
        with db_session() as session:
            session.delete(space)
