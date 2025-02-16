from aiogram.types import Message
from aiogram import Router
from aiogram.filters import CommandStart
from sqlalchemy.ext.asyncio import AsyncSession
from repository_layer.card_repository import CardRepository
from repository_layer.seen_cards_repository import SeenCardsRepository
from repository_layer.user_repository import UserRepository
from ui_layer.lexicon.lexicon_ru import lexicon_ru
from service_layer.card_service import CardService
from service_layer.user_service import UserService
from ui_layer.keyboards.start_command_keyboards import StartCommandKeyboards

router = Router()


@router.message(CommandStart())
async def start_command(message: Message, db: AsyncSession, injected_user_id: str):
    user_repository = UserRepository(db)
    card_repo = CardRepository(db)
    seen_cards_repository = SeenCardsRepository(db)

    user_service = UserService(user_repo=user_repository)
    card_service = CardService(
        card_repo=card_repo,
        user_repo=user_repository,
        seen_cards_repo=seen_cards_repository,
    )

    print(injected_user_id)

    user_cards_exist = await card_service.user_has_cards(injected_user_id)

    if user_cards_exist:
        keyboard = StartCommandKeyboards.startup_card_builder()
        response_text = lexicon_ru["start_alternative"]
    else:
        keyboard = StartCommandKeyboards.start_creating_cards()
        response_text = lexicon_ru["start"]

    await message.reply(response_text, reply_markup=keyboard)
    await user_service.ensure_user_state(injected_user_id)
