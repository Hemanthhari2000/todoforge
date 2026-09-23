from todoforge.db.schema import AppState, Space
from todoforge.db.session import db_session


class SpaceStateService:
    def set(self, space: Space):
        with db_session() as session:
            session.add(AppState(current_space_id=space.id))

    def get(self) -> Space | None:
        with db_session() as session:
            app_state = session.query(AppState).first()
            if not (app_state and app_state.current_space_id):
                return None

            current_space = session.query(Space).get(app_state.current_space_id)
            if not current_space:
                return None

            return current_space
