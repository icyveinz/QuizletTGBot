from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from ui_layer.lexicon.lexicon_ru import lexicon_ru


class CreateCardsKeyboards:
    @staticmethod
    def select_mode_for_creating():
        button_list = [
            lexicon_ru["keyboards"]["create_cards_keyboards"]["manual"],
            lexicon_ru["keyboards"]["create_cards_keyboards"]["auto"]
        ]
        kb_builder = ReplyKeyboardBuilder()
        buttons: list[KeyboardButton] = [
            KeyboardButton(text=option) for option in button_list
        ]
        for button in buttons:
            kb_builder.row(button)
        return kb_builder.as_markup(resize_keyboard=True, one_time_keyboard=True)

    @staticmethod
    def leave_mode_for_creating():
        button_list = [
            lexicon_ru["keyboards"]["create_cards_keyboards"]["finish_uploading_session"]
        ]
        kb_builder = ReplyKeyboardBuilder()
        buttons: list[KeyboardButton] = [
            KeyboardButton(text=option) for option in button_list
        ]
        for button in buttons:
            kb_builder.row(button)
        return kb_builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
