from controller import get_db
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
