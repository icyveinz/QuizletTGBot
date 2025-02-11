from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from typing import List, Optional
from entity_layer.card import Card


class CardRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def _execute_query(self, query):
        try:
            result = await self.db.execute(query)
            return result
        except SQLAlchemyError as e:
            print(f"Database error: {e}")
            return None

    async def user_has_cards(self, user_id: str) -> bool:
        result = await self._execute_query(select(Card).filter(Card.user_id == user_id))
        if result:
            return result.scalars().first() is not None
        return False

    async def get_user_cards(self, user_id: str) -> List[Card]:
        result = await self._execute_query(select(Card).filter(Card.user_id == user_id))
        return list(result.scalars()) if result else []

    async def get_next_unstudied_card(self, user_id: str) -> Optional[Card]:
        result = await self._execute_query(
            select(Card).filter_by(user_id=user_id, is_studied=False)
        )
        return result.scalars().first() if result else None

    async def reset_studied_cards(self, user_id: str) -> int:
        result = await self._execute_query(
            select(Card).filter_by(user_id=user_id, is_studied=True)
        )
        if result:
            cards_to_update = result.scalars().all()
            if cards_to_update:
                for card in cards_to_update:
                    card.is_studied = False
                await self.db.commit()
                return len(cards_to_update)
        return 0

    async def create_card(self, user_id: str, front_side: str, back_side: str) -> Optional[Card]:
        try:
            new_card = Card(user_id=user_id, front_side=front_side, back_side=back_side)
            self.db.add(new_card)
            await self.db.commit()
            return new_card
        except SQLAlchemyError as e:
            print(f"Database error: {e}")
            await self.db.rollback()
            return None

    async def create_cards(self, user_id: str, cards: List[tuple[str, str]]) -> bool:
        try:
            new_cards = [
                Card(user_id=user_id, front_side=front, back_side=back)
                for front, back in cards
            ]
            self.db.add_all(new_cards)
            await self.db.commit()
            return True
        except SQLAlchemyError as e:
            print(f"Database error: {e}")
            await self.db.rollback()
            return False

    async def get_card(self, card_id: int) -> Optional[Card]:
        result = await self._execute_query(select(Card).filter_by(id=card_id))
        return result.scalars().first() if result else None

    async def update_card(self, card: Card) -> bool:
        try:
            self.db.add(card)
            await self.db.commit()
            return True
        except SQLAlchemyError as e:
            print(f"Database error: {e}")
            await self.db.rollback()
            return False

    async def get_unstudied_card(self, user_id: str, seen_cards: List[int]) -> Optional[Card]:
        seen_card_ids = set(seen_cards)
        result = await self._execute_query(
            select(Card)
            .filter(Card.user_id == user_id, Card.id.notin_(seen_card_ids))
            .order_by(Card.is_studied.asc(), func.random())
        )
        return result.scalars().first() if result else None
