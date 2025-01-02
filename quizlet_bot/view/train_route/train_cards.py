from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from controller import get_db
from model import Card, UserStateEntity
from tools import int_to_str

def create_card_buttons(card_id, is_card_flipped):
    if not card_id:  # Check if card_id is valid
        raise ValueError("Invalid card_id provided to create_card_buttons.")

    # Create buttons
    buttons = [
        InlineKeyboardButton(
            text="Flip Card" if not is_card_flipped else "Show Front",
            callback_data=f"flip:{card_id}"
        ),
        InlineKeyboardButton(
            text="Mark as Studied",
            callback_data=f"mark_studied:{card_id}"
        ),
        InlineKeyboardButton(
            text="Next Card",
            callback_data=f"next:{card_id}"
        )
    ]

    # Return InlineKeyboardMarkup with buttons
    return InlineKeyboardMarkup(row_width=1).add(*buttons)



async def train_cards(message: types.Message):
    connection = next(get_db())
    user_id = message.from_user.id
    card = connection.query(Card).filter_by(user_id=user_id, is_studied=False).first()
    user_state = connection.query(UserStateEntity).filter_by(user_id=user_id).first()
    if not user_state:
        user_state = UserStateEntity(
            user_id=int_to_str(user_id),
            current_card_id=card.id,
            is_card_flipped=False
        )
        connection.add(user_state)
    else:
        user_state.current_card_id = card.id
        user_state.is_card_flipped = False
    connection.commit()
    keyboard = create_card_buttons(card.id, is_card_flipped=False)
    await message.answer(card.front_side, reply_markup=keyboard)