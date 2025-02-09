from db_core_layer.db_config import get_db
from entity_layer.states_enum import StatesEnum
from repository_layer.card_repository import CardRepository
from repository_layer.user_repository import UserRepository
from service_layer.card_button_service import CardButtonService


class CardService:
    def __init__(self):
        self.card_repo = CardRepository(get_db())
        self.user_repo = UserRepository(get_db())
        self.button_service = CardButtonService()

    async def user_has_cards(self, user_id: str) -> bool:
        return await self.card_repo.user_has_cards(user_id)

    async def get_user_cards(self, user_id: str):
        return await self.card_repo.get_user_cards(user_id)

    async def start_training_session(self, user_id: str):
        card = await self.card_repo.get_next_unstudied_card(user_id)
        user = await self.user_repo.get_user(user_id)
        card_condition = user.is_card_flipped
        await self.user_repo.update_user_state(user_id, StatesEnum.TRAINS_CARDS.value)
        return card, card_condition

    async def get_next_train_card(self, user_id: str):
        card = await self.card_repo.get_next_unstudied_card(user_id)
        user = await self.user_repo.get_user(user_id)
        return card, user.is_card_flipped

    async def reset_studied_cards(self, user_id: str) -> int:
        return await self.card_repo.reset_studied_cards(user_id)

    async def process_front_card_input(self, user_id: str, text: str) -> str:
        await self.user_repo.update_user_with_front_card(user_id, text)
        return "<b>Передняя сторона сохранена</b>!\n<i>Теперь введите обратную сторону.</i>"

    async def process_back_card_input(self, user_id: str, text: str) -> str:
        user_state = await self.user_repo.get_user(user_id)
        front = user_state.front_side
        await self.card_repo.create_card(user_id, front, text)
        await self.user_repo.reset_user(user_id)
        return f"<b>Карта была создана!</b>\n<i>Передняя сторона:</i> {front}\n<i>Задняя сторона:</i> {text}"

    async def handle_callback_flip_card_action(self, card_id: int, user_id: str):
        result = await self.button_service.handle_flip_button(card_id, user_id)
        return result

    async def handle_callback_next_card_action(self, card_id: int, user_id: str):
        result = await self.button_service.handle_next_button(card_id, user_id)
        return result

    async def handle_callback_mark_studied_card_action(self, card_id: int):
        result = await self.button_service.handle_mark_studied_button(card_id)
        return result
