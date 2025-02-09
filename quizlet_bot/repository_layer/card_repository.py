from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional
from db_core_layer.db_repository import get_db
from entity_layer.card import Card


class CardRepository:
    def __init__(self):
        self.db = next(get_db())

    async def user_has_cards(self, user_id: str) -> bool:
        async with self.db() as session:
            result = await session.execute(
                select(Card).filter(Card.user_id == user_id)
            )
            return result.scalars().count() > 0

    async def get_user_cards(self, user_id: str) -> List['Card']:
        try:
            async with self.db() as session:
                result = await session.execute(
                    select(Card).filter(Card.user_id == user_id)
                )
                return result.scalars().all()
        except SQLAlchemyError as e:
            print(f"Database error: {e}")
            return []

    async def get_next_unstudied_card(self, user_id: str) -> Optional[Card]:
        try:
            async with self.db() as session:
                result = await session.execute(
                    select(Card).filter_by(user_id=user_id, is_studied=False)
                )
                return result.scalars().first()
        except SQLAlchemyError as e:
            print(f"Database error: {e}")
            return None

    async def reset_studied_cards(self, user_id: str) -> int:
        try:
            async with self.db() as session:
                result = await session.execute(
                    select(Card).filter_by(user_id=user_id, is_studied=True)
                )
                updated_rows = result.update({"is_studied": False}, synchronize_session="fetch")
                await session.commit()
                return updated_rows
        except SQLAlchemyError as e:
            print(f"Database error: {e}")
            await session.rollback()
            return 0

    async def create_card(self, user_id: str, front_side: str, back_side: str) -> 'Card':
        async with self.db() as session:
            new_card = Card(user_id=user_id, front_side=front_side, back_side=back_side)
            session.add(new_card)
            await session.commit()
            return new_card

    async def get_card(self, card_id: int) -> Optional[Card]:
        async with self.db() as session:
            result = await session.execute(
                select(Card).filter_by(id=card_id)
            )
            return result.scalars().first()

    async def update_card(self, card: Card) -> None:
        async with self.db() as session:
            await session.commit()

    async def get_unstudied_cards(self, user_id: str, seen_cards_ids: List[int]) -> Optional['Card']:
        async with self.db() as session:
            result = await session.execute(
                select(Card).filter(
                    Card.user_id == user_id,
                    ~Card.id.in_(seen_cards_ids),
                    Card.is_studied.is_(False),
                )
            )
            return result.scalars().first()
