from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from ui_layer.lexicon.lexicon_ru import lexicon_ru


class TrainerInlineKeyboards:
    @staticmethod
    def create_card_buttons(card_id, is_card_flipped, difference, total_cards):
        if not card_id:
            raise ValueError("Invalid card_id provided to create_card_buttons.")

        buttons = [
            [
                InlineKeyboardButton(
                    text=(
                        lexicon_ru["keyboards"]["trainer_inline"]["counter"]
                        .format(difference=difference, total_cards=total_cards)
                    ),
                    callback_data=f"NULL:{card_id}",
                )
            ],
            [
                InlineKeyboardButton(
                    text=(
                        lexicon_ru["keyboards"]["trainer_inline"]["flip_card"]
                        if not is_card_flipped
                        else lexicon_ru["keyboards"]["trainer_inline"]["flip_inverted"]
                    ),
                    callback_data=f"FLIP:{card_id}",
                )
            ],
            [
                InlineKeyboardButton(
                    text=lexicon_ru["keyboards"]["trainer_inline"]["next_card"],
                    callback_data=f"NEXT:{card_id}",
                )
            ],
            [
                InlineKeyboardButton(
                    text=lexicon_ru["keyboards"]["trainer_inline"]["mark_studied"],
                    callback_data=f"MARK_STUDIED:{card_id}",
                )
            ],
            [
                InlineKeyboardButton(
                    text=lexicon_ru["keyboards"]["trainer_inline"]["exit"],
                    callback_data=f"EXIT:{card_id}",
                )
            ],
        ]

        return InlineKeyboardMarkup(inline_keyboard=buttons)
