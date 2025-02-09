from sqlalchemy.ext.asyncio import AsyncSession
from repository_layer.card_repository import CardRepository
from repository_layer.user_repository import UserRepository
from ui_layer.trainer_keyboards import TrainerKeyboards


class CardButtonService:
    def __init__(self, db: AsyncSession):
        self.card_repo = CardRepository(db)
        self.user_state_repo = UserRepository(db)

    async def prepare_next_card(self, user_id: str):
        user_state = await self.user_state_repo.get_user(user_id)
        seen_cards_ids = user_state.get_seen_cards()

        card = await self.card_repo.get_unstudied_cards(user_id, seen_cards_ids)
        if not card:
            return None, None

        keyboard = TrainerKeyboards.create_card_buttons(card.id, False)
        return card, keyboard

    async def handle_next_button(self, card_id: int, user_id: str):
        card = await self.card_repo.get_card(card_id)
        user_state = await self.user_state_repo.get_user(user_id)
        if not card or not user_state:
            return {"message": "Card or user state not found!"}
        return await self.prepare_next_card(user_id)

    async def handle_mark_studied_button(self, card_id: int):
        card = await self.card_repo.get_card(card_id)
        if not card:
            return {"message": "Card not found!"}

        card.is_studied = True
        await self.card_repo.update_card(card)

        return {"message": "Card marked as studied!"}

    async def handle_flip_button(self, card_id: int, user_id: str):
        print(user_id)
        card = await self.card_repo.get_card(card_id)
        user_state = await self.user_state_repo.get_user(user_id)
        print(card, user_state)
        if not card or not user_state:
            return {"message": "Card or user state not found!"}

        user_state.is_card_flipped = not user_state.is_card_flipped
        text = card.back_side if user_state.is_card_flipped else card.front_side

        keyboard = TrainerKeyboards.create_card_buttons(
            card.id, user_state.is_card_flipped
        )
        return {"message": text, "keyboard": keyboard}
