from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from db_core_layer.db_repository import get_db
from entity_layer.states_enum import StatesEnum
from entity_layer.user_state import UserStateEntity


class UserRepository:
    def __init__(self):
        self.db = next(get_db())

    async def get_user(self, user_id: str):
        async with self.db() as session:
            result = await session.execute(
                select(UserStateEntity).filter_by(user_id=user_id)
            )
            return result.scalars().first()

    async def create_user(self, user_id: str, is_card_flipped: bool):
        async with self.db() as session:
            new_state = UserStateEntity(
                user_id=user_id, is_card_flipped=is_card_flipped
            )
            session.add(new_state)
            await session.commit()
            return new_state

    async def reset_user(self, user_id: str):
        async with self.db() as session:
            user_state = await self.get_user(user_id)
            if user_state:
                user_state.state = None
                user_state.front_side = None
                await session.commit()

    async def update_user_state(self, user_id: str, state: str) -> bool:
        try:
            async with self.db() as session:
                user_state = await self.get_user(user_id)
                if user_state:
                    user_state.state = state
                    await session.commit()
                    return True
                return False
        except SQLAlchemyError as e:
            print(f"Database error: {e}")
            return False

    async def update_user_with_front_card(self, user_id: str, front: str) -> bool:
        try:
            async with self.db() as session:
                user_state = await self.get_user(user_id)
                if user_state:
                    user_state.front_side = front
                    user_state.state = StatesEnum.AWAITING_BACK.value
                    await session.commit()
                    return True
                return False
        except SQLAlchemyError as e:
            print(f"Database error: {e}")
            return False
