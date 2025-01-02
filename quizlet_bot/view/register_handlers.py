from aiogram import Dispatcher, Bot
from aiogram.filters import CommandStart
from view import train_cards
from view.train_route.train_cards import handle_card_buttons
from view.view_cards_route.view_cards import handle_view_cards_button
from view.start_route.start_command import start_command, handle_card_input, handle_create_cards_button
from functools import partial


def register_handlers(dp: Dispatcher, bot : Bot):
    dp.message.register(start_command, CommandStart())
    dp.message.register(handle_view_cards_button, lambda message: message.text == "View Cards")
    dp.message.register(handle_create_cards_button, lambda message: message.text == "Create Cards")
    dp.message.register(train_cards, lambda message: message.text == "Train Cards")
    dp.callback_query.register(partial(handle_card_buttons, bot=bot))
    dp.message.register(handle_card_input)