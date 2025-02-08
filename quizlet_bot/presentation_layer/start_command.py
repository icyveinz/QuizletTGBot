from aiogram.types import Message
from aiogram import Router
from aiogram.filters import CommandStart
from controller import get_db

router = Router()

@router.message(CommandStart())
async def start_command(message: Message):
    user_id = str(message.from_user.id)
    session = next(get_db())