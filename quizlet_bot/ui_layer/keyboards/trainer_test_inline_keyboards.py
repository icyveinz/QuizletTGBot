import random
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from ui_layer.lexicon.lexicon_ru import lexicon_ru


class TrainerTestInlineKeyboards:
    @staticmethod
    def create_answer_buttons(
        card_id: int, correct_answer: str, wrong_answers: list[str]
    ) -> InlineKeyboardMarkup:
        if not card_id:
            raise ValueError("Invalid card_id provided to create_answer_buttons.")
        if len(wrong_answers) != 3:
            raise ValueError("Exactly 3 wrong answers must be provided.")

        # Create a list of tuples (answer_text, callback_prefix)
        options = [(correct_answer, "CORRECT")]
        options.extend([(ans, "WRONG") for ans in wrong_answers])

        # Shuffle the list so the correct answer isn't always in the same position
        random.shuffle(options)

        # Create InlineKeyboardButtons for each option
        buttons = [
            [
                InlineKeyboardButton(  # Each button should be in its own list
                    text=option_text, callback_data=f"{callback_prefix}:{card_id}"
                )
            ]
            for option_text, callback_prefix in options
        ]
        buttons.append(
            [
                InlineKeyboardButton(
                text=lexicon_ru["keyboards"]["trainer_inline"]["exit"],
                callback_data=f"EXIT:{card_id}")
            ]
        )
        return InlineKeyboardMarkup(inline_keyboard=buttons)
