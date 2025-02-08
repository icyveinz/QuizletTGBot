class UserService:
    def __init__(self):
        self.user_repo = UserRepository()

    async def ensure_user_state(self, user_id: int):
        """Ensures that a user state exists in the database."""
        user_state = self.user_repo.get_user_state(user_id)
        if not user_state:
            self.user_repo.create_user_state(user_id, is_card_flipped=False)

class CardService:
    def __init__(self):
        self.card_repo = CardRepository()

    async def user_has_cards(self, user_id: int) -> bool:
        """Checks if a user has created any cards."""
        return self.card_repo.user_has_cards(user_id)
