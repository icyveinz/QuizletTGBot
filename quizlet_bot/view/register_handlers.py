from aiogram import Dispatcher, Bot
from view import train_cards, reset_trained_cards_route
from view.train_route.train_cards import handle_card_buttons
from view.view_cards_route.view_cards import handle_view_cards_button
from view.start_route.start_command import (
    handle_card_input,
    handle_create_cards_button,
)
from functools import partial
from presentation_layer.start_command import router as start_command_router


def register_handlers(dp: Dispatcher, bot: Bot):
    dp.include_router(start_command_router)
    dp.message.register(
        handle_view_cards_button, lambda message: message.text == "View Cards"
    )
    dp.message.register(
        handle_create_cards_button, lambda message: message.text == "Create Cards"
    )
    dp.message.register(train_cards, lambda message: message.text == "Train Cards")
    dp.message.register(
        reset_trained_cards_route, lambda message: message.text == "Reset Trained Cards"
    )
    dp.callback_query.register(partial(handle_card_buttons, bot=bot))
    dp.message.register(handle_card_input)
