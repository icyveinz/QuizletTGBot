from db_core_layer.db_config import get_db
from repository_layer.user_repository import UserRepository


class UserService:
    def __init__(self):
        self.user_repo = UserRepository(get_db())

    async def ensure_user_state(self, user_id: str):
        user_state = await self.user_repo.get_user(user_id)
        if not user_state:
            await self.user_repo.create_user(user_id, is_card_flipped=False)

    async def update_user_state(self, user_id: str, state: str) -> bool:
        return await self.user_repo.update_user_state(user_id, state)
