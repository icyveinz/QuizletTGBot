from aiogram import Router
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from entity_layer.enums.states_enum import StatesEnum
from filter_layer.user_state_filter import (
    UserStateFilter,
)
from repository_layer.card_repository import CardRepository
from repository_layer.seen_cards_repository import SeenCardsRepository
from repository_layer.user_repository import UserRepository
from service_layer.card_service import CardService
from ui_layer.keyboards.start_command_keyboards import StartCommandKeyboards

router = Router()


@router.message(UserStateFilter(StatesEnum.AWAITING_FRONT.value))
async def handle_card_input(message: Message, db: AsyncSession, injected_user_id: str):
    card_repo = CardRepository(db)
    user_repo = UserRepository(db)
    seen_cards_repo = SeenCardsRepository(db)

    card_service = CardService(
        card_repo=card_repo, seen_cards_repo=seen_cards_repo, user_repo=user_repo
    )

    text = message.text.strip()

    response = await card_service.process_front_card_input(injected_user_id, text)

    await message.reply(response)


@router.message(UserStateFilter(StatesEnum.AWAITING_BACK.value))
async def handle_back_card_input(
    message: Message, db: AsyncSession, injected_user_id: str
):
    card_repo = CardRepository(db)
    user_repo = UserRepository(db)
    seen_cards_repo = SeenCardsRepository(db)

    card_service = CardService(
        card_repo=card_repo, seen_cards_repo=seen_cards_repo, user_repo=user_repo
    )

    text = message.text.strip()

    response = await card_service.process_back_card_input(injected_user_id, text)

    await message.reply(
        response, reply_markup=StartCommandKeyboards.startup_card_builder()
    )
