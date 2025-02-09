from aiogram import Bot
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from repository_layer.card_repository import CardRepository
from repository_layer.user_repository import UserRepository


class CardButtonService:
    def __init__(self):
        self.card_repo = CardRepository()
        self.user_state_repo = UserRepository()

    async def prepare_next_card(self, user_id: str):
        user_state = self.user_state_repo.get_user(user_id)
        seen_cards_ids = user_state.get_seen_cards()

        card = self.card_repo.get_unstudied_cards(user_id, seen_cards_ids)
        if not card:
            return None, None

        keyboard = self.create_card_buttons(card.id, False)
        return card, keyboard

    async def handle_card_action(
        self, action: str, card_id: int, user_id: str, bot: Bot
    ):
        card = self.card_repo.get_card(card_id)
        user_state = self.user_state_repo.get_user(user_id)

        if not card or not user_state:
            return {"message": "Card or user state not found!"}

        if action == "flip":
            user_state.is_card_flipped = not user_state.is_card_flipped
            self.user_state_repo.update_user_state(user_state)
            text = card.back_side if user_state.is_card_flipped else card.front_side
            keyboard = self.create_card_buttons(card.id, user_state.is_card_flipped)
            return {"message": text, "keyboard": keyboard}

        elif action == "mark_studied":
            card.is_studied = True
            self.card_repo.update_card(card)
            return {"message": "Card marked as studied!"}

        elif action == "next":
            return await self.prepare_next_card(user_id)

    def create_card_buttons(self, card_id, is_card_flipped):
        buttons = [
            [
                InlineKeyboardButton(
                    text="Flip Card" if not is_card_flipped else "Show Front",
                    callback_data=f"flip:{card_id}",
                )
            ],
            [
                InlineKeyboardButton(
                    text="Mark as Studied", callback_data=f"mark_studied:{card_id}"
                )
            ],
            [InlineKeyboardButton(text="Next Card", callback_data=f"next:{card_id}")],
        ]

        return InlineKeyboardMarkup(inline_keyboard=buttons)
