from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession


class CallbackExitCondition(BaseFilter):
    async def __call__(
        self, callback_query: CallbackQuery, db: AsyncSession, injected_user_id: str
    ) -> bool:
        try:
            return callback_query.data.startswith("EXIT:")
        except Exception as e:
            print(f"Error in CallbackCardsTrainerNextCondition: {e}")
            return False
