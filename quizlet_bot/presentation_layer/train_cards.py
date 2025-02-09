from aiogram import Router, F
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from service_layer.card_service import CardService
from ui_layer.trainer_keyboards import TrainerKeyboards

router = Router()


@router.message(F.text == "Train Cards")
async def train_cards_handler(message: Message, db: AsyncSession):
    card_service = CardService(db)
    user_id = str(message.from_user.id)

    card, is_flipped = await card_service.start_training_session(user_id)

    if not card:
        await message.answer("No more cards to study!")
        return

    keyboard = TrainerKeyboards.create_card_buttons(card.id, is_card_flipped=is_flipped)
    await message.answer(card.front_side, reply_markup=keyboard)
