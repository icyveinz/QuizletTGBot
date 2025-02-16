from aiogram import Dispatcher, Bot
from presentation_layer.start_command import router as start_command_router
from presentation_layer.view_cards_button import router as view_cards_button_router
from presentation_layer.create_cards_button import router as create_cards_button_router
from presentation_layer.train_cards import router as train_cards_button_router
from presentation_layer.reset_trained_cards import router as reset_trained_cards_router
from presentation_layer.handle_card_input import router as handle_card_input_router
from presentation_layer.handle_card_buttons import router as handle_card_buttons_router
from presentation_layer.handle_test_buttons import router as handle_test_buttons_router
from presentation_layer.handle_exit_callback import router as handle_exit_callback_router


def register_handlers(dp: Dispatcher, bot: Bot):
    dp.include_router(start_command_router)
    dp.include_router(view_cards_button_router)
    dp.include_router(create_cards_button_router)
    dp.include_router(train_cards_button_router)
    dp.include_router(reset_trained_cards_router)
    dp.include_router(handle_card_input_router)
    dp.include_router(handle_card_buttons_router)
    dp.include_router(handle_test_buttons_router)
    dp.include_router(handle_exit_callback_router)
