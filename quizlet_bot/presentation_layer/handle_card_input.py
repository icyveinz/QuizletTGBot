from aiogram import Router
from aiogram.types import Message
from entity_layer.states_enum import StatesEnum
from filter_layer.handle_card_input import (
    HandleCardInputFilter,
)
from service_layer.card_service import CardService

router = Router()
card_service = CardService()


@router.message(HandleCardInputFilter(StatesEnum.AWAITING_FRONT.value))
async def handle_card_input(message: Message):
    user_id = str(message.from_user.id)
    text = message.text.strip()

    response = await card_service.process_front_card_input(user_id, text)

    await message.reply(response)


@router.message(HandleCardInputFilter(StatesEnum.AWAITING_BACK.value))
async def handle_back_card_input(message: Message):
    user_id = str(message.from_user.id)
    text = message.text.strip()

    response = await card_service.process_back_card_input(user_id, text)

    await message.reply(response)
