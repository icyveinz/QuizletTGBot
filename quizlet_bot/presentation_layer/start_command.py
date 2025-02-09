from aiogram.types import Message
from aiogram import Router
from aiogram.filters import CommandStart
from sqlalchemy.ext.asyncio import AsyncSession
from service_layer.card_service import CardService
from service_layer.user_service import UserService
from ui_layer.start_command_keyboards import StartCommandKeyboards

router = Router()


@router.message(CommandStart())
async def start_command(message: Message, db: AsyncSession):
    user_id = str(message.from_user.id)

    user_service = UserService(db)
    card_service = CardService(db)

    user_cards_exist = await card_service.user_has_cards(user_id)

    if user_cards_exist:
        keyboard = StartCommandKeyboards.startup_card_builder()
        response_text = "Welcome back! You already have cards. Use the buttons below to view or create more."
    else:
        keyboard = StartCommandKeyboards.start_creating_cards()
        response_text = (
            "You don't have any cards yet. Would you like to create your first cards?"
        )

    await message.reply(response_text, reply_markup=keyboard)
    await user_service.ensure_user_state(user_id)
