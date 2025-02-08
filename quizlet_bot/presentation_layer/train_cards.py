from aiogram import Router, F, types
from aiogram.types import Message
from service_layer.card_service import CardService
from ui_layer.keyboard_factory import KeyboardFactory

router = Router()
card_service = CardService()

@router.message(F.text == "Train Cards")
async def train_cards_handler(message: Message):
    user_id = str(message.from_user.id)

    card, is_flipped = await card_service.get_next_train_card(user_id)

    if not card:
        await message.answer("No more cards to study!")
        return

    keyboard = KeyboardFactory.create_card_buttons(card.id, is_card_flipped=is_flipped)
    await message.answer(card.front_side, reply_markup=keyboard)
