from aiogram import Bot, Router
from aiogram.types import CallbackQuery

from service_layer.card_service import CardService

router = Router()
card_service = CardService()

@router.callback_query()
async def handle_card_buttons(callback_query: CallbackQuery, bot: Bot):
    action, card_id = callback_query.data.split(":")
    card_id = int(card_id)
    user_id = callback_query.from_user.id
    response = await card_service.handle_card_action(action, card_id, user_id, bot)
    await callback_query.answer(response['message'])