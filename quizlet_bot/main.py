import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from db_core_layer.db_config import init_db
from middleware_layer.db_middleware import DBInjectorMiddleware
from middleware_layer.user_id_extractor import UserIDExtractorMiddleware
from register_handlers import register_handlers

TOKEN = "6907074579:AAFJOtvMEDN8ewOVP4XnxOxWyZY-OTjLXXM"


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    await init_db()

    dp.update.middleware(DBInjectorMiddleware())
    dp.update.middleware(UserIDExtractorMiddleware())

    register_handlers(dp, bot)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
