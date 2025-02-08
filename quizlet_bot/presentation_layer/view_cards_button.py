from aiogram import Router, F, types
from aiogram.types import Message
from service_layer.card_service import CardService

router = Router()


@router.message(F.text == "View Cards")
async def handle_view_cards_button(message: Message):
    user_id = message.from_user.id
    card_service = CardService()

    user_cards = await card_service.get_user_cards(user_id)

    if user_cards:
        response = "Here are your cards:\n\n"
        for index, card in enumerate(user_cards):
            response += (
                f"{index + 1})\nАверс: {card.front_side}\nРеверс: {card.back_side}\n\n"
            )
    else:
        response = "You don't have any cards yet. Use the 'Create Cards' button to add new cards."

    await message.reply(response)
