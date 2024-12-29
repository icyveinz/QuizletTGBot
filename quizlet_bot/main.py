# main.py
import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from controller.mysql_orm_controller import engine, create_tables, Base
from controller.mysql_orm_controller.initialize_database import initialize_database
from view import start_command
from view.start_route.start_command import register_start_command

# Initialize the database
initialize_database(engine=engine)
create_tables(engine=engine, Base=Base)

TOKEN = "6907074579:AAFJOtvMEDN8ewOVP4XnxOxWyZY-OTjLXXM"

async def main() -> None:
    # Initialize Bot instance
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    # Register handlers
    register_start_command(dp)

    # Start polling
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
