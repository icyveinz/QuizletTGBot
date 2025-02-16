from aiogram import Router
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from filter_layer.callback_cards_trainer import (
    CallbackCardsTrainerFlipCondition,
    CallbackCardsTrainerMarkStudiedCondition,
    CallbackCardsTrainerNextCondition,
)
from infrastructure_layer.service_factory import (
    create_card_button_service,
)

router = Router()


@router.callback_query(CallbackCardsTrainerFlipCondition())
async def handle_flip_card_button(
    callback_query: CallbackQuery, db: AsyncSession, injected_user_id: str
):
    card_service = create_card_button_service(db)

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
    card_service = create_card_button_service(db)

    _, card_id = callback_query.data.split(":")
    card_id = int(card_id)
    response = await card_service.handle_mark_studied_button_callback(
        card_id, injected_user_id
    )
    if "message" in response:
        text = response["message"]
        keyboard = response["keyboard"]
        await callback_query.message.edit_text(text, reply_markup=keyboard)

    await callback_query.answer()


@router.callback_query(CallbackCardsTrainerNextCondition())
async def handle_next_card_button(
    callback_query: CallbackQuery, db: AsyncSession, injected_user_id: str
):
    card_service = create_card_button_service(db)

    _, card_id = callback_query.data.split(":")
    card_id = int(card_id)
    response = await card_service.handle_next_button_callback(card_id, injected_user_id)
    if "message" in response:
        text = response["message"]
        keyboard = response["keyboard"]
        await callback_query.message.edit_text(text, reply_markup=keyboard)

    await callback_query.answer()
