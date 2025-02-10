from sqlalchemy import Column, String, Text, Integer, ForeignKey, Boolean
from db_core_layer.db_config import Base


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
    seen_card_ids = Column(Text, default="", nullable=False)
