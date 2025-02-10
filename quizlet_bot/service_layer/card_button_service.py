from sqlalchemy.ext.asyncio import AsyncSession
from repository_layer.card_repository import CardRepository
from repository_layer.seen_cards_repository import SeenCardsRepository
from repository_layer.user_repository import UserRepository
from ui_layer.trainer_keyboards import TrainerKeyboards


class CardButtonService:
    def __init__(self, db: AsyncSession):
        self.card_repo = CardRepository(db)
        self.user_state_repo = UserRepository(db)
        self.seen_cards_repo = SeenCardsRepository(db)

    async def handle_callback_flip_card_action(self, card_id: int, user_id: str):
        result = await self.handle_flip_button(card_id, user_id)
        return result

    async def handle_callback_next_card_action(self, card_id: int, user_id: str):
        result = await self.handle_next_button(card_id, user_id)
        return result

    async def handle_callback_mark_studied_card_action(self, card_id: int):
        result = await self.handle_mark_studied_button(card_id)
        return result

    async def handle_next_button(self, card_id: int, user_id: str):
        card = await self.card_repo.get_card(card_id)
        user_state = await self.user_state_repo.get_user(user_id)
        if not card or not user_state:
            return {"message": "Card or user state not found!"}

        await self.seen_cards_repo.mark_card_as_seen(user_id, card_id)
        seen_cards = await self.seen_cards_repo.get_list_of_related_and_seen_cards(
            user_id
        )

        next_card = await self.card_repo.get_unstudied_card(user_id, seen_cards)

        if next_card:
            print(next_card.back_side, next_card.front_side)
            keyboard = TrainerKeyboards.create_card_buttons(
                next_card.id, user_state.is_card_flipped
            )
            return {"message": next_card.front_side, "keyboard": keyboard}
        return {"message": "You're out of cards"}

    async def handle_mark_studied_button(self, card_id: int):
        card = await self.card_repo.get_card(card_id)
        if not card:
            return {"message": "Card not found!"}

        card.is_studied = True
        await self.card_repo.update_card(card)

        return {"message": "Card marked as studied!"}

    async def handle_flip_button(self, card_id: int, user_id: str):
        card = await self.card_repo.get_card(card_id)
        user_state = await self.user_state_repo.get_user(user_id)
        if not card or not user_state:
            return {"message": "Card or user state not found!"}

        await self.user_state_repo.toggle_user_is_card_flipped(user_id)

        text = card.back_side if user_state.is_card_flipped else card.front_side

        keyboard = TrainerKeyboards.create_card_buttons(
            card.id, user_state.is_card_flipped
        )
        return {"message": text, "keyboard": keyboard}
