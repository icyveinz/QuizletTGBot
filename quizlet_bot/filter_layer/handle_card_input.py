from aiogram.filters import BaseFilter
from aiogram.types import Message
from repository_layer.user_repository import UserRepository


class HandleFrontCardInputFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        user_id = str(message.from_user.id)
        try:
            user_repo = UserRepository()
            answer = user_repo.get_user_state(user_id).state
            if answer == "AWAITING_FRONT":
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return False


class HandleBackCardInputFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        user_id = str(message.from_user.id)
        try:
            user_repo = UserRepository()
            answer = user_repo.get_user_state(user_id).state
            if answer == "AWAITING_BACK":
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return False
