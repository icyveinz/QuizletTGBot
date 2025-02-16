from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint, String

from db_core_layer.db_config import Base


class SeenCardsEntity(Base):
    __tablename__ = "seen_cards"

    id = Column(Integer, primary_key=True, autoincrement=True)
    related_card_id = Column(
        Integer, ForeignKey("cards.id", ondelete="CASCADE"), nullable=False
    )
    related_user_id = Column(
        String(50),
        ForeignKey("user_states.user_id", ondelete="CASCADE"),
        nullable=False,
    )

    # Ensures each pair is unique
    __table_args__ = (
        UniqueConstraint("related_card_id", "related_user_id", name="uq_seen_cards"),
    )
