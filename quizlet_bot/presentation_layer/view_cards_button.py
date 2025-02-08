from aiogram import Router, F
from aiogram.types import Message
from service_layer.card_service import CardService

router = Router()
card_service = CardService()


@router.message(F.text == "View Cards")
async def handle_view_cards_button(message: Message):
    user_id = str(message.from_user.id)

    user_cards = await card_service.get_user_cards(user_id)

    if user_cards:
        response = "<b>Ваши добавленные карты:</b>\n\n"
        for index, card in enumerate(user_cards):
            response += f"{index + 1})\n<b>Аверс:</b> {card.front_side}\n<i>Реверс:</i> {card.back_side}\n\n"
    else:
        response = "You don't have any cards yet. Use the 'Create Cards' button to add new cards."

    await message.reply(response)
