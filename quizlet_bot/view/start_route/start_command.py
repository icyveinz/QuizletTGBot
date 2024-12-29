# view/start_route/start_command.py
from aiogram import types, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from sqlalchemy.exc import SQLAlchemyError
from controller import get_db
from model import Card

async def start_command(message: types.Message):
    user_id = message.from_user.id  # Telegram user ID
    session = next(get_db())  # Use `next()` to get the session instance

    try:
        # Check if cards exist for the user
        user_cards = session.query(Card).filter(Card.user_id == user_id).all()

        if user_cards:
            await message.reply("Welcome back! You already have cards. Use /view_cards to see them.")
        else:
            # Suggest creating cards
            keyboard = ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text="Create Cards")],
                ],
                resize_keyboard=True
            )
            await message.reply(
                "You don't have any cards yet. Would you like to create your first cards?",
                reply_markup=keyboard
            )
    except SQLAlchemyError as e:
        await message.reply("An error occurred while accessing the database. Please try again later.")
        print(f"Database error: {e}")
    finally:
        session.close()  # Close the DB session

# Register the handler
def register_start_command(dp: Dispatcher):
    dp.message.register(start_command, CommandStart())