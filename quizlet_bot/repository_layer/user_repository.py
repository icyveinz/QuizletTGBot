from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from entity_layer.states_enum import StatesEnum
from typing import Optional

from entity_layer.user_state import UserStateEntity


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def _execute_query(self, stmt):
        try:
            result = await self.db.execute(stmt)
            return result.scalars().first()
        except SQLAlchemyError as e:
            print(f"Database error: {e}")
            return None

    async def get_user(self, user_id: str) -> Optional[UserStateEntity]:
        stmt = select(UserStateEntity).filter_by(user_id=user_id)
        return await self._execute_query(stmt)

    async def create_user(self, user_id: str, is_card_flipped: bool) -> Optional[UserStateEntity]:
        try:
            new_state = UserStateEntity(user_id=user_id, is_card_flipped=is_card_flipped)
            self.db.add(new_state)
            await self.db.commit()
            return new_state
        except SQLAlchemyError as e:
            print(f"Database error while creating user: {e}")
            await self.db.rollback()
            return None

    async def reset_user(self, user_id: str) -> bool:
        user_state = await self.get_user(user_id)
        if user_state:
            user_state.state = None
            user_state.front_side = None
            await self.db.commit()
            return True
        return False

    async def update_user_state(self, user_id: str, state: str) -> bool:
        user_state = await self.get_user(user_id)
        if user_state:
            user_state.state = state
            await self.db.commit()
            return True
        return False

    async def toggle_user_is_card_flipped(self, user_id: str) -> bool:
        user_state = await self.get_user(user_id)
        if user_state:
            user_state.is_card_flipped = not user_state.is_card_flipped
            await self.db.commit()
            return True
        return False

    async def update_user_with_front_card(self, user_id: str, front: str) -> bool:
        user_state = await self.get_user(user_id)
        if user_state:
            user_state.front_side = front
            user_state.state = StatesEnum.AWAITING_BACK.value
            await self.db.commit()
            return True
        return False
