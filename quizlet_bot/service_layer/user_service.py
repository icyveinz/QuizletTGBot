from domain_layer.repository.i_user_repository import IUserRepository


class UserService:
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    async def ensure_user_state(self, user_id: str) -> None:
        user_state = await self.user_repo.get_user(user_id)
        if not user_state:
            await self.user_repo.create_user(user_id, is_card_flipped=False)

    async def update_user_state(self, user_id: str, state: str) -> bool:
        return await self.user_repo.update_user_state(user_id, state)
