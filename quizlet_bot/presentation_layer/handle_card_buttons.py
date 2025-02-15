from aiogram import Router
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from entity_layer.states_enum import StatesEnum
from filter_layer.callback_cards_trainer import (
    CallbackCardsTrainerFlipCondition,
    CallbackCardsTrainerMarkStudiedCondition,
    CallbackCardsTrainerNextCondition,
    CallbackCardsTrainerExitCondition,
)
from service_layer.card_button_service import CardButtonService
from service_layer.user_service import UserService
from ui_layer.keyboards.start_command_keyboards import StartCommandKeyboards
from ui_layer.lexicon.lexicon_ru import lexicon_ru

router = Router()


@router.callback_query(CallbackCardsTrainerFlipCondition())
async def handle_flip_card_button(callback_query: CallbackQuery, db: AsyncSession, injected_user_id: str):
    card_service = CardButtonService(db)
    _, card_id = callback_query.data.split(":")
    card_id = int(card_id)

    response = await card_service.handle_flip_button_callback(card_id, injected_user_id)

    if "message" in response:
        text = response["message"]
        keyboard = response["keyboard"]
        await callback_query.message.edit_text(text, reply_markup=keyboard)
    await callback_query.answer()


@router.callback_query(CallbackCardsTrainerMarkStudiedCondition())
async def handle_mark_studied_card_button(
    callback_query: CallbackQuery, db: AsyncSession, injected_user_id: str
):
    card_service = CardButtonService(db)
    _, card_id = callback_query.data.split(":")
    card_id = int(card_id)
    response = await card_service.handle_mark_studied_button_callback(card_id, injected_user_id)
    if "message" in response:
        text = response["message"]
        keyboard = response["keyboard"]
        await callback_query.message.edit_text(text, reply_markup=keyboard)

    await callback_query.answer()


@router.callback_query(CallbackCardsTrainerNextCondition())
async def handle_next_card_button(callback_query: CallbackQuery, db: AsyncSession, injected_user_id: str):
    card_service = CardButtonService(db)
    _, card_id = callback_query.data.split(":")
    card_id = int(card_id)
    response = await card_service.handle_next_button_callback(card_id, injected_user_id)
    if "message" in response:
        text = response["message"]
        keyboard = response["keyboard"]
        await callback_query.message.edit_text(text, reply_markup=keyboard)

    await callback_query.answer()


@router.callback_query(CallbackCardsTrainerExitCondition())
async def handle_exit_card_button(callback_query: CallbackQuery, db: AsyncSession, injected_user_id: str):
    user_service = UserService(db)
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
