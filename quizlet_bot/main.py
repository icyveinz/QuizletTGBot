import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, html, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

# Bot token can be obtained via https://t.me/BotFather
TOKEN = "6907074579:AAFJOtvMEDN8ewOVP4XnxOxWyZY-OTjLXXM"

# Initialize Dispatcher
dp = Dispatcher()

# Sample flashcards data
flashcards = [
    {"question": "What is the capital of France?", "answer": "Paris"},
    {"question": "What is 2 + 2?", "answer": "4"},
    {"question": "What is the largest planet?", "answer": "Jupiter"},
]

# Track the current flashcard index and flip state for each user
user_data = {}


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    # Initialize user data
    user_data[message.from_user.id] = {"index": 0, "flipped": False}

    # Show the first flashcard
    await show_flashcard(message)


async def show_flashcard(message: Message):
    user_id = message.from_user.id

    # Initialize user data if it doesn't exist
    if user_id not in user_data:
        user_data[user_id] = {"index": 0, "flipped": False}

    index = user_data[user_id]["index"]
    flipped = user_data[user_id]["flipped"]

    # Get the current flashcard
    flashcard = flashcards[index]

    # Prepare the text (question or answer)
    text = flashcard["answer"] if flipped else flashcard["question"]

    # Create the inline keyboard
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Flip", callback_data="flip")],
        [
            InlineKeyboardButton(text="⬅️ Previous", callback_data="prev"),
            InlineKeyboardButton(text="Next ➡️", callback_data="next")
        ]
    ])

    # Check if we need to edit the message
    if "flashcard_message_id" in user_data[user_id]:
        message_id = user_data[user_id]["flashcard_message_id"]
        try:
            # Get the current message content
            current_message = await message.bot.get_message(message.chat.id, message_id)

            # Only update if the text or keyboard differs
            if current_message.text != text or current_message.reply_markup != keyboard:
                await message.bot.edit_message_text(
                    chat_id=message.chat.id,
                    message_id=message_id,
                    text=text,
                    reply_markup=keyboard
                )
        except Exception as e:
            logging.error(f"Failed to edit message: {e}")
    else:
        msg = await message.answer(text, reply_markup=keyboard)
        user_data[user_id]["flashcard_message_id"] = msg.message_id



@dp.callback_query()
async def handle_button_click(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id

    # Initialize user data if it doesn't exist
    if user_id not in user_data:
        user_data[user_id] = {"index": 0, "flipped": False}

    data = callback_query.data

    # Handle button actions
    if data == "flip":
        user_data[user_id]["flipped"] = not user_data[user_id]["flipped"]
    elif data == "next":
        user_data[user_id]["index"] = (user_data[user_id]["index"] + 1) % len(flashcards)
        user_data[user_id]["flipped"] = False
    elif data == "prev":
        user_data[user_id]["index"] = (user_data[user_id]["index"] - 1) % len(flashcards)
        user_data[user_id]["flipped"] = False

    # Show the updated flashcard
    await show_flashcard(callback_query.message)
    await callback_query.answer()


async def main() -> None:
    # Initialize Bot instance with default bot properties
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # Start polling
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())