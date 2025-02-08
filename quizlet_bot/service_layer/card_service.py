from repository_layer.card_repository import CardRepository


class CardService:
    def __init__(self):
        self.card_repo = CardRepository()

    async def user_has_cards(self, user_id: str) -> bool:
        return self.card_repo.user_has_cards(user_id)
