from aiogram.filters import BaseFilter
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from repository_layer.user_repository import UserRepository

class HandleCardInputFilter(BaseFilter):
    def __init__(self, expected_state: str):
        self.expected_state = expected_state

    async def __call__(self, message: Message, db: AsyncSession) -> bool:
        user_id = str(message.from_user.id)
        try:
            user_repo = UserRepository(db)
            user = await user_repo.get_user(user_id)
            return user and user.state == self.expected_state
        except Exception as e:
            print(f"Error in HandleCardInputFilter: {e}")
            return False
