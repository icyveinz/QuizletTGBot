from aiogram import Router
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from entity_layer.enums.states_enum import StatesEnum
from filter_layer.callback_exit_condition import CallbackExitCondition
from infrastructure_layer.service_factory import create_user_service
from ui_layer.keyboards.start_command_keyboards import StartCommandKeyboards
from ui_layer.lexicon.lexicon_ru import lexicon_ru

router = Router()

@router.callback_query(CallbackExitCondition())
async def handle_exit_card_button(
    callback_query: CallbackQuery, db: AsyncSession, injected_user_id: str
):
    user_service = create_user_service(db)

    response = await user_service.update_user_state(
        injected_user_id, StatesEnum.ZERO_STATE.value
    )
    await callback_query.answer()
    await callback_query.message.delete()
    if response:
        await callback_query.message.answer(
            text=lexicon_ru["train_mode"]["exit_mode"],
            reply_markup=StartCommandKeyboards.startup_card_builder(),
        )
    else:
        await callback_query.message.answer(
            text=lexicon_ru["train_mode"]["exit_mode_error"],
            reply_markup=StartCommandKeyboards.startup_card_builder(),
        )