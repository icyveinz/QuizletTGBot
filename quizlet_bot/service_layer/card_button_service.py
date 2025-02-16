from sqlalchemy.ext.asyncio import AsyncSession
from repository_layer.card_repository import CardRepository
from repository_layer.seen_cards_repository import SeenCardsRepository
from repository_layer.user_repository import UserRepository
from ui_layer.keyboards.trainer_inline_keyboards import TrainerInlineKeyboards
from ui_layer.lexicon.lexicon_ru import lexicon_ru


class CardButtonService:
    def __init__(self, db: AsyncSession):
        self.card_repo = CardRepository(db)
        self.user_state_repo = UserRepository(db)
        self.seen_cards_repo = SeenCardsRepository(db)

    async def _get_card_and_user_state(self, card_id: int, user_id: str):
        card = await self.card_repo.get_card(card_id)
        user_state = await self.user_state_repo.get_user(user_id)
        if not card or not user_state:
            return None, None
        return card, user_state

    async def get_progress_counter(self, user_id: str) -> (int, int):
        trained_cards = await self.card_repo.count_studied_cards(user_id)
        total_cards = await self.card_repo.count_all_user_cards(user_id)
        difference = total_cards - trained_cards
        passed = total_cards - difference
        return passed, total_cards

    async def _get_next_card_and_keyboard(
        self, user_id: str, seen_cards: list, is_card_flipped: bool
    ):
        next_card = await self.card_repo.get_unstudied_card(user_id, seen_cards)
        if not next_card:
            return None, None
        difference, total_cards = await self.get_progress_counter(user_id)
        keyboard = TrainerInlineKeyboards.create_card_buttons(
            next_card.id, is_card_flipped, difference, total_cards
        )
        return next_card, keyboard

    async def handle_next_button_callback(self, card_id: int, user_id: str):
        card, user_state = await self._get_card_and_user_state(card_id, user_id)
        if not card or not user_state:
            return {"message": lexicon_ru["train_mode"]["error_card_user_state"]}

        await self.seen_cards_repo.mark_card_as_seen(user_id, card_id)
        seen_cards = await self.seen_cards_repo.get_list_of_related_and_seen_cards(
            user_id
        )

        next_card, keyboard = await self._get_next_card_and_keyboard(
            user_id, seen_cards, user_state.is_card_flipped
        )

        if next_card:
            return {"message": next_card.front_side, "keyboard": keyboard}
        else:
            return {
                "message": lexicon_ru["train_mode"]["all_cards_viewed"],
                "keyboard": None,
            }

    async def handle_mark_studied_button_callback(self, card_id: int, user_id: str):
        card, user_state = await self._get_card_and_user_state(card_id, user_id)
        if not card:
            return {"message": lexicon_ru["train_mode"]["error_card"]}

        card.is_studied = True
        await self.card_repo.update_card(card)

        await self.seen_cards_repo.mark_card_as_seen(user_id, card_id)
        seen_cards = await self.seen_cards_repo.get_list_of_related_and_seen_cards(
            user_id
        )

        next_card, keyboard = await self._get_next_card_and_keyboard(
            user_id, seen_cards, user_state.is_card_flipped
        )

        if next_card:
            return {"message": next_card.front_side, "keyboard": keyboard}
        else:
            return {"message": lexicon_ru["train_mode"]["success"], "keyboard": None}

    async def handle_flip_button_callback(self, card_id: int, user_id: str):
        card, user_state = await self._get_card_and_user_state(card_id, user_id)
        if not card or not user_state:
            return {"message": lexicon_ru["train_mode"]["error_card_user_state"]}

        await self.user_state_repo.toggle_user_is_card_flipped(user_id)
        difference, total_cards = await self.get_progress_counter(user_id)
        text = card.back_side if user_state.is_card_flipped else card.front_side
        keyboard = TrainerInlineKeyboards.create_card_buttons(
            card.id, user_state.is_card_flipped, difference, total_cards
        )

        return {"message": text, "keyboard": keyboard}
