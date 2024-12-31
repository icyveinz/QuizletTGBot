from aiogram import types
from sqlalchemy.exc import SQLAlchemyError

from controller import get_db
from model import Card


async def handle_view_cards_button(message: types.Message):
    user_id = str(message.from_user.id)
    session = next(get_db())

    try:
        user_cards = session.query(Card).filter(Card.user_id == user_id).all()

        if user_cards:
            response = "Here are your cards:\n\n"
            for index, card in enumerate(user_cards):
                response += f"{index + 1})\nАверс: {card.front_side}\nРеверс: {card.back_side}\n\n"
            await message.reply(response)
        else:
            await message.reply("You don't have any cards yet. Use the 'Create Cards' button to add new cards.")
    except SQLAlchemyError as e:
        await message.reply("An error occurred while fetching your cards. Please try again later.")
        print(f"Database error: {e}")
    finally:
        session.close()