from aiogram import Bot
from repository_layer.card_repository import CardRepository
from repository_layer.user_repository import UserRepository
from service_layer.card_button_service import CardButtonService


class CardService:
    def __init__(self):
        self.card_repo = CardRepository()
        self.user_repo = UserRepository()
        self.button_service = CardButtonService()

    async def user_has_cards(self, user_id: str) -> bool:
        return self.card_repo.user_has_cards(user_id)

    async def get_user_cards(self, user_id: str):
        return self.card_repo.get_user_cards(user_id)

    async def get_next_train_card(self, user_id: str):
        card = self.card_repo.get_next_unstudied_card(user_id)
        if not card:
            return None, False

        user_state = self.user_repo.get_user_state(user_id)
        if not user_state:
            self.user_repo.create_user_state(user_id, card.id)
            is_flipped = False
        else:
            self.user_repo.update_user_state(user_id, card.id, is_card_flipped=False)
            is_flipped = user_state.is_card_flipped

        return card, is_flipped

    async def reset_studied_cards(self, user_id: str) -> int:
        return self.card_repo.reset_studied_cards(user_id)

    async def process_card_input(self, user_id: str, text: str) -> str:
        user_state = self.user_repo.get_user_state(user_id)

        if not user_state or not user_state.state:
            return "Please press the 'Create Cards' button first to create a card."

        if user_state.state == "AWAITING_FRONT":
            self.user_repo.update_user_state(user_id, state="AWAITING_BACK")
            return "Front side saved! Now, please enter the back side of the card."

        elif user_state.state == "AWAITING_BACK":
            front = user_state.front_side
            self.card_repo.create_card(user_id, front, text)

            # Reset user state
            self.user_repo.reset_user_state(user_id)
            return f"Card created!\nFront: {front}\nBack: {text}"

        return (
            "Unexpected state. Please press the 'Create Cards' button again to restart."
        )

    async def handle_card_action(self, action: str, card_id: int, user_id: int, bot: Bot):
        result = await self.button_service.handle_card_action(action, card_id, user_id, bot)
        return result
