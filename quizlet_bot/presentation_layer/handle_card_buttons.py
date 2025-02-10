from aiogram import Router
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from filter_layer.callback_cards_trainer import (
    CallbackCardsTrainerFlipCondition,
    CallbackCardsTrainerMarkStudiedCondition,
    CallbackCardsTrainerNextCondition,
)
from service_layer.card_button_service import CardButtonService

router = Router()


@router.callback_query(CallbackCardsTrainerFlipCondition())
async def handle_flip_card_button(callback_query: CallbackQuery, db: AsyncSession):
    user_id = str(callback_query.from_user.id)
    card_service = CardButtonService(db)
    _, card_id = callback_query.data.split(":")
    card_id = int(card_id)

    response = await card_service.handle_callback_flip_card_action(card_id, user_id)

    if "message" in response:
        text = response["message"]
        keyboard = response["keyboard"]

    await callback_query.message.edit_text(text, reply_markup=keyboard)
    await callback_query.answer()


@router.callback_query(CallbackCardsTrainerMarkStudiedCondition())
async def handle_mark_studied_card_button(
    callback_query: CallbackQuery, db: AsyncSession
):
    user_id = str(callback_query.from_user.id)
    card_service = CardButtonService(db)
    _, card_id = callback_query.data.split(":")
    card_id = int(card_id)
    response = await card_service.handle_callback_mark_studied_card_action(
        card_id, user_id
    )
    if "message" in response:
        text = response["message"]
        keyboard = response["keyboard"]

    await callback_query.message.edit_text(text, reply_markup=keyboard)
    await callback_query.answer()


@router.callback_query(CallbackCardsTrainerNextCondition())
async def handle_next_card_button(callback_query: CallbackQuery, db: AsyncSession):
    user_id = str(callback_query.from_user.id)
    card_service = CardButtonService(db)
    _, card_id = callback_query.data.split(":")
    card_id = int(card_id)
    response = await card_service.handle_callback_next_card_action(card_id, user_id)
    if "message" in response:
        text = response["message"]
        keyboard = response["keyboard"]

    await callback_query.message.edit_text(text, reply_markup=keyboard)
    await callback_query.answer()
