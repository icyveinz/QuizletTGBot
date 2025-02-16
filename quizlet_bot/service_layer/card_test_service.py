from domain_layer.repository.i_card_repository import ICardRepository
from domain_layer.repository.i_seen_cards_repository import ISeenCardsRepository
from domain_layer.repository.i_user_repository import IUserRepository
from ui_layer.keyboards.trainer_test_inline_keyboards import TrainerTestInlineKeyboards
from ui_layer.lexicon.lexicon_ru import lexicon_ru
from typing import List


class CardTestService:
    def __init__(
        self,
        card_repo: ICardRepository,
        user_state_repo: IUserRepository,
        seen_cards_repo: ISeenCardsRepository
    ):
        self.card_repo = card_repo
        self.user_state_repo = user_state_repo
        self.seen_cards_repo = seen_cards_repo

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

    async def _get_next_card_and_keyboard(self, user_id: str, seen_cards: List[int]):
        next_card = await self.card_repo.get_unstudied_card(user_id, seen_cards)
        fake_answers = await self.card_repo.get_random_back_sides(user_id)
        if not next_card:
            return None, None
        difference, total_cards = await self.get_progress_counter(user_id)
        keyboard = TrainerTestInlineKeyboards.create_answer_buttons(
            next_card.id, next_card.back_side, fake_answers, difference, total_cards
        )
        return next_card, keyboard

    async def handle_false_answer_button_callback(self, card_id: int, user_id: str):
        card, user_state = await self._get_card_and_user_state(card_id, user_id)
        if not card or not user_state:
            return {"message": lexicon_ru["train_mode"]["error_card_user_state"]}

        await self.seen_cards_repo.mark_card_as_seen(user_id, card_id)
        seen_cards = await self.seen_cards_repo.get_list_of_related_and_seen_cards(user_id)

        next_card, keyboard = await self._get_next_card_and_keyboard(user_id, seen_cards)

        if next_card:
            return {"message": next_card.front_side, "keyboard": keyboard}
        else:
            return {
                "message": lexicon_ru["train_mode"]["all_cards_viewed"],
                "keyboard": None,
            }

    async def handle_true_answer_button_callback(self, card_id: int, user_id: str):
        card, user_state = await self._get_card_and_user_state(card_id, user_id)
        if not card:
            return {"message": lexicon_ru["train_mode"]["error_card"]}

        card.is_studied = True
        await self.card_repo.update_card(card)

        await self.seen_cards_repo.mark_card_as_seen(user_id, card_id)
        seen_cards = await self.seen_cards_repo.get_list_of_related_and_seen_cards(user_id)

        next_card, keyboard = await self._get_next_card_and_keyboard(user_id, seen_cards)

        if next_card:
            return {"message": next_card.front_side, "keyboard": keyboard}
        else:
            return {"message": lexicon_ru["train_mode"]["success"], "keyboard": None}
