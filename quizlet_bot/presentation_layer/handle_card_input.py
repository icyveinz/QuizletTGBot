from aiogram import Router
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from domain_layer.enums.states_enum import StatesEnum
from filter_layer.user_state_filter import (
    UserStateFilter,
)
from infrastructure_layer.service_factory import create_card_service
from ui_layer.keyboards.start_command_keyboards import StartCommandKeyboards

router = Router()


@router.message(UserStateFilter(StatesEnum.AWAITING_FRONT.value))
async def handle_card_input(message: Message, db: AsyncSession, injected_user_id: str):
    card_service = create_card_service(db)
    text = message.text.strip()
    response = await card_service.process_front_card_input(injected_user_id, text)
    await message.reply(response)


@router.message(UserStateFilter(StatesEnum.AWAITING_BACK.value))
async def handle_back_card_input(
    message: Message, db: AsyncSession, injected_user_id: str
):
    card_service = create_card_service(db)
    text = message.text.strip()
    response = await card_service.process_back_card_input(injected_user_id, text)
    await message.reply(
        response, reply_markup=StartCommandKeyboards.startup_card_builder()
    )
