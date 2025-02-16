from sqlalchemy.ext.asyncio import AsyncSession
from repository_layer.card_repository import CardRepository
from repository_layer.seen_cards_repository import SeenCardsRepository
from repository_layer.user_repository import UserRepository
from service_layer.card_button_service import CardButtonService
from service_layer.card_service import CardService
from service_layer.card_test_service import CardTestService
from service_layer.user_service import UserService


def create_card_service(db: AsyncSession) -> CardService:
    card_repo = CardRepository(db)
    user_repo = UserRepository(db)
    seen_cards_repo = SeenCardsRepository(db)
    return CardService(
        card_repo=card_repo, seen_cards_repo=seen_cards_repo, user_repo=user_repo
    )


def create_user_service(db: AsyncSession) -> UserService:
    user_repository = UserRepository(db)
    return UserService(user_repo=user_repository)


def create_card_button_service(db: AsyncSession) -> CardButtonService:
    user_state_repo = UserRepository(db)
    seen_cards_repo = SeenCardsRepository(db)
    card_repo = CardRepository(db)
    return CardButtonService(
        user_state_repo=user_state_repo,
        seen_cards_repo=seen_cards_repo,
        card_repo=card_repo,
    )


def create_card_test_service(db: AsyncSession) -> CardTestService:
    card_repo = CardRepository(db)
    user_state_repo = UserRepository(db)
    seen_cards_repo = SeenCardsRepository(db)
    return CardTestService(
        card_repo=card_repo,
        seen_cards_repo=seen_cards_repo,
        user_state_repo=user_state_repo,
    )
