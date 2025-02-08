from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram import Router
from aiogram.filters import CommandStart
from service_layer.card_service import CardService
from service_layer.user_service import UserService

router = Router()

@router.message(CommandStart())
async def start_command(message: Message):
    user_id = str(message.from_user.id)
    user_service = UserService()
    card_service = CardService()

    user_cards_exist = await card_service.user_has_cards(user_id)

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    if user_cards_exist:
        keyboard.add(KeyboardButton(text="View Cards"))
        keyboard.add(KeyboardButton(text="Create Cards"))
        keyboard.add(KeyboardButton(text="Train Cards"))
        keyboard.add(KeyboardButton(text="Reset Trained Cards"))
        response_text = "Welcome back! You already have cards. Use the buttons below to view or create more."
    else:
        keyboard.add(KeyboardButton(text="Create Cards"))
        response_text = "You don't have any cards yet. Would you like to create your first cards?"

    await message.reply(response_text, reply_markup=keyboard)

    # Initialize user state if not present
    await user_service.ensure_user_state(user_id)
