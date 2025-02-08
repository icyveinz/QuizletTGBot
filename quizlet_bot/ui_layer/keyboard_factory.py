from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class KeyboardFactory:
    @staticmethod
    def create_card_buttons(card_id, is_card_flipped):
        if not card_id:
            raise ValueError("Invalid card_id provided to create_card_buttons.")

        buttons = [
            [
                InlineKeyboardButton(
                    text="Flip Card" if not is_card_flipped else "Show Front",
                    callback_data=f"flip:{card_id}",
                )
            ],
            [
                InlineKeyboardButton(
                    text="Mark as Studied", callback_data=f"mark_studied:{card_id}"
                )
            ],
            [InlineKeyboardButton(text="Next Card", callback_data=f"next:{card_id}")],
        ]

        return InlineKeyboardMarkup(inline_keyboard=buttons)
