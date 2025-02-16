from aiogram.types import Message
from aiogram import Router
from aiogram.filters import CommandStart
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure_layer.service_factory import (
    create_user_service,
    create_card_service,
)
from ui_layer.lexicon.lexicon_ru import lexicon_ru
from ui_layer.keyboards.start_command_keyboards import StartCommandKeyboards

router = Router()


@router.message(CommandStart())
async def start_command(message: Message, db: AsyncSession, injected_user_id: str):
    user_service = create_user_service(db)
    card_service = create_card_service(db)

    user_cards_exist = await card_service.user_has_cards(injected_user_id)

    if user_cards_exist:
        keyboard = StartCommandKeyboards.startup_card_builder()
        response_text = lexicon_ru["start_alternative"]
    else:
        keyboard = StartCommandKeyboards.start_creating_cards()
        response_text = lexicon_ru["start"]

    await message.reply(response_text, reply_markup=keyboard)
    await user_service.ensure_user_state(injected_user_id)
