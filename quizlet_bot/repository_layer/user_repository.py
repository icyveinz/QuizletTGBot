from sqlalchemy.exc import SQLAlchemyError
from db_core_layer.db_repository import get_db
from entity_layer.user_state import UserStateEntity


class UserRepository:
    def __init__(self):
        self.db = next(get_db())

    def get_user_state(self, user_id: str):
        return self.db.query(UserStateEntity).filter_by(user_id=user_id).first()

    def create_user_state(self, user_id: str, is_card_flipped: bool):
        new_state = UserStateEntity(user_id=user_id, is_card_flipped=is_card_flipped)
        self.db.add(new_state)
        self.db.commit()
        return new_state

    def reset_user_state(self, user_id: str):
        user_state = self.get_user_state(user_id)
        if user_state:
            user_state.state = None
            user_state.front_side = None
            self.db.commit()

    def update_user_state(self, user_id: str, state: str) -> bool:
        try:
            user_state = (
                self.db.query(UserStateEntity).filter_by(user_id=user_id).first()
            )
            if user_state:
                user_state.state = state
                self.db.commit()
                return True
            return False
        except SQLAlchemyError as e:
            print(f"Database error: {e}")
            return False
        finally:
            self.db.close()
