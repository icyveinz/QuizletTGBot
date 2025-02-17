from abc import ABC, abstractmethod
from typing import Optional
from domain_layer.db_models.user_state import UserStateEntity


class IUserRepository(ABC):
    @abstractmethod
    async def get_user(self, user_id: str) -> Optional[UserStateEntity]:
        pass

    @abstractmethod
    async def create_user(
        self, user_id: str, is_card_flipped: bool
    ) -> Optional[UserStateEntity]:
        pass

    @abstractmethod
    async def reset_user(self, user_id: str) -> bool:
        pass

    @abstractmethod
    async def update_user_state(self, user_id: str, state: str) -> bool:
        pass

    @abstractmethod
    async def toggle_user_is_card_flipped(self, user_id: str) -> bool:
        pass

    @abstractmethod
    async def update_user_with_front_card(self, user_id: str, front: str) -> bool:
        pass
