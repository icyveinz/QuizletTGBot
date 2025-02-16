from abc import ABC, abstractmethod
from typing import List


class ISeenCardsRepository(ABC):
    @abstractmethod
    async def mark_card_as_seen(self, user_id: str, card_id: int) -> bool:
        pass

    @abstractmethod
    async def get_list_of_related_and_seen_cards(self, user_id: str) -> List[int]:
        pass

    @abstractmethod
    async def clean_seen_cards_by_user_id(self, user_id: str) -> bool:
        pass
