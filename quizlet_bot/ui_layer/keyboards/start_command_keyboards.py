from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from ui_layer.lexicon.lexicon_ru import lexicon_ru


class StartCommandKeyboards:

    @staticmethod
    def startup_card_builder():
        button_list = [
            lexicon_ru["keyboards"]["start_keyboard"]["view_cards"],
            lexicon_ru["keyboards"]["start_keyboard"]["create_cards"],
            lexicon_ru["keyboards"]["start_keyboard"]["train_cards"],
            lexicon_ru["keyboards"]["start_keyboard"]["reset_trained_cards"],
        ]
        kb_builder = ReplyKeyboardBuilder()
        buttons: list[KeyboardButton] = [
            KeyboardButton(text=option) for option in button_list
        ]
        for button in buttons:
            kb_builder.row(button)
        return kb_builder.as_markup(resize_keyboard=True, one_time_keyboard=True)

    @staticmethod
    def start_creating_cards():
        button_list = [lexicon_ru["keyboards"]["start_keyboard"]["create_cards"]]
        kb_builder = ReplyKeyboardBuilder()
        buttons: list[KeyboardButton] = [
            KeyboardButton(text=option) for option in button_list
        ]
        kb_builder.add(*buttons)
        return kb_builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
