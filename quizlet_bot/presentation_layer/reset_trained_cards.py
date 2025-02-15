from aiogram import Router, F
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from ui_layer.lexicon.lexicon_ru import lexicon_ru
from service_layer.card_service import CardService
from ui_layer.keyboards.start_command_keyboards import StartCommandKeyboards

router = Router()


@router.message(
    F.text == lexicon_ru["keyboards"]["start_keyboard"]["reset_trained_cards"]
)
async def reset_trained_cards_handler(
    message: Message, db: AsyncSession, injected_user_id: str
):
    card_service = CardService(db)

    await card_service.reset_seen_cards(injected_user_id)
    reset_count = await card_service.reset_studied_cards(injected_user_id)

    if reset_count > 0:
        await message.reply(
            lexicon_ru["reset_trained_cards_success"].format(count=reset_count),
            reply_markup=StartCommandKeyboards.startup_card_builder(),
        )
    else:
        await message.reply(
            lexicon_ru["reset_trained_cards"],
            reply_markup=StartCommandKeyboards.startup_card_builder(),
        )
