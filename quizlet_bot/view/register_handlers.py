from aiogram import Dispatcher
from aiogram.filters import CommandStart

from view.view_cards_route.view_cards import handle_view_cards_button
from view.start_route.start_command import start_command, handle_card_input, handle_create_cards_button


def register_handlers(dp: Dispatcher):
    dp.message.register(start_command, CommandStart())
    dp.message.register(handle_view_cards_button, lambda message: message.text == "View Cards")
    dp.message.register(handle_create_cards_button, lambda message: message.text == "Create Cards")
    dp.message.register(handle_card_input)