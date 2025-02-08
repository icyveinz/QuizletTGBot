from aiogram import Router, F
from aiogram.types import Message
from service_layer.card_service import CardService

router = Router()
card_service = CardService()


@router.message(F.text == "Reset Trained Cards")
async def reset_trained_cards_handler(message: Message):
    user_id = str(message.from_user.id)

    reset_count = await card_service.reset_studied_cards(user_id)

    if reset_count > 0:
        await message.reply(
            f"{reset_count} cards were reset so you can review them again."
        )
    else:
        await message.reply("No studied cards found to reset.")
