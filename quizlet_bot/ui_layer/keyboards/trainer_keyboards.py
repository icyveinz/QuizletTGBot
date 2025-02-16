from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from ui_layer.lexicon.lexicon_ru import lexicon_ru


class TrainerKeyboard:
    @staticmethod
    def entry_builder():
        button_list = [
            lexicon_ru["keyboards"]["trainer_keyboard"]["classic"],
            lexicon_ru["keyboards"]["trainer_keyboard"]["test"],
        ]
        kb_builder = ReplyKeyboardBuilder()
        buttons: list[KeyboardButton] = [
            KeyboardButton(text=option) for option in button_list
        ]
        for button in buttons:
            kb_builder.row(button)
        return kb_builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
