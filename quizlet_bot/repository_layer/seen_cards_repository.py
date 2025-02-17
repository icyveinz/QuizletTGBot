from sqlalchemy import delete
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from domain_layer.interfaces.i_seen_cards_repository import ISeenCardsRepository
from domain_layer.db_models.seen_cards_entity import SeenCardsEntity
from typing import List


class SeenCardsRepository(ISeenCardsRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def mark_card_as_seen(self, user_id: str, card_id: int) -> bool:
        try:
            stmt = (
                insert(SeenCardsEntity)
                .values(related_user_id=user_id, related_card_id=card_id)
                .on_conflict_do_nothing()
            )
            await self.db.execute(stmt)
            await self.db.commit()
            return True
        except SQLAlchemyError as e:
            print(f"Database error while marking card as seen: {e}")
            await self.db.rollback()
            return False

    async def get_list_of_related_and_seen_cards(self, user_id: str) -> List[int]:
        try:
            result = await self.db.execute(
                select(SeenCardsEntity.related_card_id).filter_by(
                    related_user_id=user_id
                )
            )
            seen_card_ids = result.scalars().all()
            return list(seen_card_ids)
        except SQLAlchemyError as e:
            print(f"Database error while retrieving seen cards: {e}")
            return []

    async def clean_seen_cards_by_user_id(self, user_id: str) -> bool:
        try:
            await self.db.execute(
                delete(SeenCardsEntity).filter_by(related_user_id=user_id)
            )
            await self.db.commit()
            return True
        except SQLAlchemyError as e:
            print(f"Database error while cleaning seen cards: {e}")
            await self.db.rollback()
            return False
