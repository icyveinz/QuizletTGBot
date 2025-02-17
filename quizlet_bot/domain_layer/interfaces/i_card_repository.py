from abc import ABC, abstractmethod
from typing import List, Optional
from domain_layer.db_models.card import Card


class ICardRepository(ABC):
    @abstractmethod
    async def user_has_cards(self, user_id: str) -> bool:
        pass

    @abstractmethod
    async def get_user_cards(self, user_id: str) -> List[Card]:
        pass

    @abstractmethod
    async def get_next_unstudied_card(self, user_id: str) -> Optional[Card]:
        pass

    @abstractmethod
    async def count_studied_cards(self, user_id: str) -> int:
        pass

    @abstractmethod
    async def count_all_user_cards(self, user_id: str) -> int:
        pass

    @abstractmethod
    async def reset_studied_cards(self, user_id: str) -> int:
        pass

    @abstractmethod
    async def create_card(
        self, user_id: str, front_side: str, back_side: str
    ) -> Optional[Card]:
        pass

    @abstractmethod
    async def create_cards(self, user_id: str, cards: List[tuple[str, str]]) -> bool:
        pass

    @abstractmethod
    async def get_card(self, card_id: int) -> Optional[Card]:
        pass

    @abstractmethod
    async def update_card(self, card: Card) -> bool:
        pass

    @abstractmethod
    async def get_unstudied_card(
        self, user_id: str, seen_cards: List[int]
    ) -> Optional[Card]:
        pass

    @abstractmethod
    async def get_random_back_sides(self, user_id: str) -> List[str]:
        pass
