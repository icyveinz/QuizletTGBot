import json
from sqlalchemy import Column, String, Text, Integer, ForeignKey, Boolean
from controller import Base


class UserStateEntity(Base):
    __tablename__ = "user_states"
    user_id = Column(String(50), nullable=False, primary_key=True)
    state = Column(String(50), default=None, nullable=True)
    front_side = Column(Text, default=None, nullable=True)
    back_side = Column(Text, default=None, nullable=True)
    current_card_id = Column(
        Integer, ForeignKey("cards.id"), default=None, nullable=True
    )
    is_card_flipped = Column(Boolean, default=False, nullable=False)
    seen_card_ids = Column(Text, default="[]", nullable=False)

    def get_seen_card(self):
        return json.loads(self.seen_card_ids)

    def add_seen_card(self, card_id):
        seen_cards = self.get_seen_card()
        if card_id not in seen_cards:
            seen_cards.append(card_id)
            self.seen_card_ids = json.dumps(seen_cards)

    def reset_seen_cards(self):
        self.seen_card_ids = json.dumps([])


