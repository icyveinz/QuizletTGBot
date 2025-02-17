from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from domain_layer.enums.states_enum import StatesEnum
from repository_layer.user_repository import UserRepository


class CallbackCardsTestTrainerTrue(BaseFilter):
    async def __call__(
        self, callback_query: CallbackQuery, db: AsyncSession, injected_user_id: str
    ) -> bool:
        try:
            user_repo = UserRepository(db)
            user_state = (await user_repo.get_user(injected_user_id)).state
            return (
                callback_query.data.startswith("CORRECT:")
                and user_state == StatesEnum.TESTING_CARDS.value
            )
        except Exception as e:
            print(f"Error in CallbackCardsTestTrainerTrue: {e}")
            return False


class CallbackCardsTestTrainerFalse(BaseFilter):
    async def __call__(
        self, callback_query: CallbackQuery, db: AsyncSession, injected_user_id: str
    ) -> bool:
        try:
            user_repo = UserRepository(db)
            user_state = (await user_repo.get_user(injected_user_id)).state
            return (
                callback_query.data.startswith("WRONG:")
                and user_state == StatesEnum.TESTING_CARDS.value
            )
        except Exception as e:
            print(f"Error in CallbackCardsTestTrainerFalse: {e}")
            return False
