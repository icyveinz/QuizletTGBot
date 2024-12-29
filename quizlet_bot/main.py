import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from sqlalchemy.exc import SQLAlchemyError
from controller import get_db
from controller.mysql_orm_controller import engine, create_tables, Base
from controller.mysql_orm_controller.initialize_database import initialize_database

from model import Card

# Initialize the database
initialize_database(engine=engine)
create_tables(engine=engine, Base=Base)

TOKEN = "6907074579:AAFJOtvMEDN8ewOVP4XnxOxWyZY-OTjLXXM"

# Initialize Dispatcher
dp = Dispatcher()


@dp.message(CommandStart())
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



async def main() -> None:
    # Initialize Bot instance with default bot properties
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # Start polling
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())