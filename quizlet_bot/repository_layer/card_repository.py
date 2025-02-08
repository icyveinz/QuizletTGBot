from typing import List

from sqlalchemy.exc import SQLAlchemyError
from controller import get_db
from entity_layer.card import Card


class CardRepository:
    def __init__(self):
        self.db = next(get_db())

    def user_has_cards(self, user_id: str) -> bool:
        return self.db.query(Card).filter(Card.user_id == user_id).count() > 0

    def get_user_cards(self, user_id: int) -> List[Card]:
        try:
            return self.db.query(Card).filter(Card.user_id == user_id).all()
        except SQLAlchemyError as e:
            print(f"Database error: {e}")
            return []
        finally:
            self.db.close()
