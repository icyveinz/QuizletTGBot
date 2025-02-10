from aiogram import Router
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from entity_layer.states_enum import StatesEnum
from filter_layer.user_state_filter import (
    UserStateFilter,
)
from service_layer.card_service import CardService

router = Router()


@router.message(UserStateFilter(StatesEnum.AWAITING_FRONT.value))
async def handle_card_input(message: Message, db: AsyncSession):
    card_service = CardService(db)
    user_id = str(message.from_user.id)
    text = message.text.strip()

    response = await card_service.process_front_card_input(user_id, text)

    await message.reply(response)


@router.message(UserStateFilter(StatesEnum.AWAITING_BACK.value))
async def handle_back_card_input(message: Message, db: AsyncSession):
    card_service = CardService(db)
    user_id = str(message.from_user.id)
    text = message.text.strip()

    response = await card_service.process_back_card_input(user_id, text)

    await message.reply(response)
