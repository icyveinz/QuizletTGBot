from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


class CreateCardsKeyboards:
    @staticmethod
    def select_mode_for_creating():
        button_list = ["Добавить вручную", "Загрузить пакетом"]
        kb_builder = ReplyKeyboardBuilder()
        buttons: list[KeyboardButton] = [
            KeyboardButton(text=option) for option in button_list
        ]
        for button in buttons:
            kb_builder.row(button)
        return kb_builder.as_markup(resize_keyboard=True, one_time_keyboard=True)

    @staticmethod
    def leave_mode_for_creating():
        button_list = ["Завершить добавление"]
        kb_builder = ReplyKeyboardBuilder()
        buttons: list[KeyboardButton] = [
            KeyboardButton(text=option) for option in button_list
        ]
        for button in buttons:
            kb_builder.row(button)
        return kb_builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
