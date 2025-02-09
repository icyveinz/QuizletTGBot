from aiogram import Router
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from filter_layer.callback_cards_trainer import (
    CallbackCardsTrainerFlipCondition,
    CallbackCardsTrainerMarkStudiedCondition,
    CallbackCardsTrainerNextCondition,
)
from service_layer.card_service import CardService

router = Router()


@router.callback_query(CallbackCardsTrainerFlipCondition())
async def handle_flip_card_button(callback_query: CallbackQuery, db: AsyncSession):
    card_service = CardService(db)
    action, card_id = callback_query.data.split(":")
    card_id = int(card_id)
    response = await card_service.handle_callback_flip_card_action(card_id, action)
    await callback_query.answer(response["message"])


@router.callback_query(CallbackCardsTrainerMarkStudiedCondition())
async def handle_mark_studied_card_button(
    callback_query: CallbackQuery, db: AsyncSession
):
    card_service = CardService(db)
    _, card_id = callback_query.data.split(":")
    card_id = int(card_id)
    response = await card_service.handle_callback_mark_studied_card_action(card_id)
    await callback_query.answer(response["message"])


@router.callback_query(CallbackCardsTrainerNextCondition())
async def handle_next_card_button(callback_query: CallbackQuery, db: AsyncSession):
    card_service = CardService(db)
    action, card_id = callback_query.data.split(":")
    card_id = int(card_id)
    response = await card_service.handle_callback_next_card_action(card_id, action)
    await callback_query.answer(response["message"])
