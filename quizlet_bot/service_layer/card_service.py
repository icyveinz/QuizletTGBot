from repository_layer.card_repository import CardRepository
from repository_layer.user_repository import UserRepository


class CardService:
    def __init__(self):
        self.card_repo = CardRepository()
        self.user_repo = UserRepository()

    async def user_has_cards(self, user_id: str) -> bool:
        return self.card_repo.user_has_cards(user_id)

    async def get_user_cards(self, user_id: str):
        return self.card_repo.get_user_cards(user_id)

    async def get_next_train_card(self, user_id: str):
        card = self.card_repo.get_next_unstudied_card(user_id)
        if not card:
            return None, False

        # Update user training state
        user_state = self.user_repo.get_user_state(user_id)
        if not user_state:
            self.user_repo.create_user_state(user_id, card.id)
            is_flipped = False
        else:
            self.user_repo.update_user_state(user_id, card.id, is_card_flipped=False)
            is_flipped = user_state.is_card_flipped

        return card, is_flipped
