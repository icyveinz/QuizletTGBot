from aiogram import Router
from aiogram.types import Message
from service_layer.card_service import CardService

router = Router()
card_service = CardService()


@router.message()
async def handle_card_input(message: Message):
    user_id = str(message.from_user.id)
    text = message.text.strip()

    response = await card_service.process_card_input(user_id, text)

    await message.reply(response)
