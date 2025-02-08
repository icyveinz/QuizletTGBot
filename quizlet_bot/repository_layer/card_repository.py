from controller import get_db
from entity_layer.card import Card


class CardRepository:
    def __init__(self):
        self.db = next(get_db())

    def user_has_cards(self, user_id: str) -> bool:
        return self.db.query(Card).filter(Card.user_id == user_id).count() > 0
