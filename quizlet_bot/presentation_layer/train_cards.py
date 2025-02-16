from aiogram import Router, F
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from entity_layer.states_enum import StatesEnum
from filter_layer.user_state_filter import UserStateFilter
from service_layer.card_button_service import CardButtonService
from service_layer.card_service import CardService
from service_layer.user_service import UserService
from ui_layer.keyboards.trainer_inline_keyboards import TrainerInlineKeyboards
from ui_layer.keyboards.trainer_keyboards import TrainerKeyboard
from ui_layer.lexicon.lexicon_ru import lexicon_ru

router = Router()


@router.message(F.text == lexicon_ru["keyboards"]["start_keyboard"]["train_cards"])
async def enter_training_mode(
    message: Message, db: AsyncSession, injected_user_id: str
):
    user_service = UserService(db)

    await user_service.update_user_state(
        injected_user_id, StatesEnum.CHOOSING_TRAINING_MODE.value
    )

    await message.reply(
        text=lexicon_ru["train_mode"]["entry"],
        reply_markup=TrainerKeyboard.entry_builder(),
    )


@router.message(
    F.text == lexicon_ru["keyboards"]["trainer_keyboard"]["classic"],
    UserStateFilter(StatesEnum.CHOOSING_TRAINING_MODE.value),
)
async def classic_card_training_mode(
    message: Message, db: AsyncSession, injected_user_id: str
):
    card_service = CardService(db)
    card_button_service = CardButtonService(db)

    await card_service.reset_seen_cards(injected_user_id)
    card, is_flipped = await card_service.start_training_session(injected_user_id)
    difference, total_cards = await card_button_service.get_progress_counter(
        injected_user_id
    )

    if not card:
        await message.answer(lexicon_ru["train_mode"]["no_more_cards_to_study"])
        return

    keyboard = TrainerInlineKeyboards.create_card_buttons(
        card.id,
        is_card_flipped=is_flipped,
        difference=difference,
        total_cards=total_cards,
    )
    await message.answer(card.front_side, reply_markup=keyboard)
