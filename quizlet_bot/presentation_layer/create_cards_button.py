from aiogram import Router, F, types
from aiogram.types import Message
from service_layer.user_service import UserService

router = Router()
user_service = UserService()

@router.message(F.text == "Create Cards")
async def handle_create_cards_button(message: Message):
    user_id = str(message.from_user.id)

    success = await user_service.update_user_state(user_id, "AWAITING_FRONT")

    if success:
        await message.reply("Please enter the front side of the card.")
    else:
        await message.reply("An error occurred. Please try again later.")
