from aiogram import Router, F
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from service_layer.card_service import CardService
from ui_layer.keyboards.trainer_keyboards import TrainerKeyboards
from ui_layer.lexicon.lexicon_ru import lexicon_ru

router = Router()


@router.message(F.text == lexicon_ru["keyboards"]["start_keyboard"]["train_cards"])
async def train_cards_handler(message: Message, db: AsyncSession):
    card_service = CardService(db)
    user_id = str(message.from_user.id)

    await card_service.reset_seen_cards(user_id)
    card, is_flipped = await card_service.start_training_session(user_id)

    if not card:
        await message.answer(lexicon_ru["train_mode"]["no_more_cards_to_study"])
        return

    keyboard = TrainerKeyboards.create_card_buttons(card.id, is_card_flipped=is_flipped)
    await message.answer(card.front_side, reply_markup=keyboard)
