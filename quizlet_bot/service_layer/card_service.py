from sqlalchemy.ext.asyncio import AsyncSession
from entity_layer.states_enum import StatesEnum
from repository_layer.card_repository import CardRepository
from repository_layer.seen_cards_repository import SeenCardsRepository
from repository_layer.user_repository import UserRepository
from ui_layer.lexicon.lexicon_ru import lexicon_ru
from utilities.parser import trim_content_to_cards


class CardService:
    def __init__(self, db: AsyncSession):
        self.card_repo = CardRepository(db)
        self.user_repo = UserRepository(db)
        self.seen_cards_repo = SeenCardsRepository(db)

    async def _get_user_and_card(self, user_id: str):
        card = await self.card_repo.get_next_unstudied_card(user_id)
        user = await self.user_repo.get_user(user_id)
        return card, user

    async def user_has_cards(self, user_id: str) -> bool:
        return await self.card_repo.user_has_cards(user_id)

    async def get_user_cards(self, user_id: str):
        return await self.card_repo.get_user_cards(user_id)

    async def start_training_session(self, user_id: str):
        card, user = await self._get_user_and_card(user_id)
        if not card:
            return lexicon_ru["train_mode"]["no_more_cards_to_study"]

        await self.user_repo.update_user_state(user_id, StatesEnum.TRAINS_CARDS.value)
        return card, user.is_card_flipped

    async def get_next_train_card(self, user_id: str):
        card, user = await self._get_user_and_card(user_id)
        if not card:
            return lexicon_ru["train_mode"]["no_more_cards_to_study"]

        return card, user.is_card_flipped

    async def reset_studied_cards(self, user_id: str) -> int:
        return await self.card_repo.reset_studied_cards(user_id)

    async def process_front_card_input(self, user_id: str, text: str) -> str:
        await self.user_repo.update_user_with_front_card(user_id, text)
        return lexicon_ru["card_service"]["front_input"]

    async def process_back_card_input(self, user_id: str, text: str) -> str:
        user_state = await self.user_repo.get_user(user_id)
        front = user_state.front_side
        await self.card_repo.create_card(user_id, front, text)
        await self.user_repo.reset_user(user_id)
        return lexicon_ru["card_service"]["input_result"].format(front=front, text=text)

    async def reset_seen_cards(self, user_id: str):
        await self.seen_cards_repo.clean_seen_cards_by_user_id(user_id)

    async def add_user_set(self, user_id: str, text: str) -> str:
        converted_cards = trim_content_to_cards(text)
        result = await self.card_repo.create_cards(user_id, converted_cards)
        if result:
            return lexicon_ru["card_service"]["add_user_set_result"].format(
                converted_cards=len(converted_cards)
            )
        else:
            return lexicon_ru["card_service"]["error_card"]
