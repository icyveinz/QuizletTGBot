from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


class StartCommandKeyboards:

    @staticmethod
    def startup_card_builder():
        button_list = ["View Cards", "Create Cards", "Train Cards", "Reset Trained Cards"]
        kb_builder = ReplyKeyboardBuilder()
        buttons: list[KeyboardButton] = [
            KeyboardButton(text=option) for option in button_list
        ]
        kb_builder.add(*buttons)
        return kb_builder.as_markup(resize_keyboard=True)

    @staticmethod
    def start_creating_cards():
        button_list = ["Create Cards"]
        kb_builder = ReplyKeyboardBuilder()
        buttons: list[KeyboardButton] = [
            KeyboardButton(text=option) for option in button_list
        ]
        kb_builder.add(*buttons)
        return kb_builder.as_markup(resize_keyboard=True)