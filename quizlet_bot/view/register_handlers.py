from aiogram import Dispatcher, Bot
from view import train_cards, reset_trained_cards_route
from view.train_route.train_cards import handle_card_buttons
from view.start_route.start_command import handle_card_input
from functools import partial
from presentation_layer.start_command import router as start_command_router
from presentation_layer.view_cards_button import router as view_cards_button_router
from presentation_layer.create_cards_button import router as create_cards_button_router


def register_handlers(dp: Dispatcher, bot: Bot):
    dp.include_router(start_command_router)
    dp.include_router(view_cards_button_router)
    dp.include_router(create_cards_button_router)
    dp.message.register(train_cards, lambda message: message.text == "Train Cards")
    dp.message.register(
        reset_trained_cards_route, lambda message: message.text == "Reset Trained Cards"
    )
    dp.callback_query.register(partial(handle_card_buttons, bot=bot))
    dp.message.register(handle_card_input)
