from aiogram import types, Bot
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from controller import get_db
from model import Card, UserStateEntity
from tools import int_to_str


def create_card_buttons(card_id, is_card_flipped):
    if not card_id:  # Check if card_id is valid
        raise ValueError("Invalid card_id provided to create_card_buttons.")

    # Create buttons
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

    # Return InlineKeyboardMarkup with button rows
    return InlineKeyboardMarkup(inline_keyboard=buttons)


async def train_cards(message: types.Message):
    connection = next(get_db())
    user_id = message.from_user.id

    card = connection.query(Card).filter_by(user_id=user_id, is_studied=False).first()

    user_state = connection.query(UserStateEntity).filter_by(user_id=user_id).first()
    if not user_state:
        user_state = UserStateEntity(
            user_id=int_to_str(user_id),
            current_card_id=card.id if card else None,
            is_card_flipped=False,
        )
        connection.add(user_state)
    else:
        user_state.current_card_id = card.id if card else None
        user_state.is_card_flipped = False

    connection.commit()

    if not card:
        await message.answer("No more cards to study!")
        return

    keyboard = create_card_buttons(card.id, is_card_flipped=False)
    await message.answer(card.front_side, reply_markup=keyboard)


async def handle_card_buttons(callback_query: types.CallbackQuery, bot: Bot):
    connection = next(get_db())

    action, card_id = callback_query.data.split(":")
    card_id = int(card_id)
    user_id = int_to_str(callback_query.from_user.id)

    card = connection.query(Card).filter_by(id=card_id).first()
    user_state = connection.query(UserStateEntity).filter_by(user_id=user_id).first()

    if not card or not user_state:
        await callback_query.answer("Error: Card or state not found!")
        return

    if action == "flip":
        user_state.is_card_flipped = not user_state.is_card_flipped
        connection.commit()
        text = card.back_side if user_state.is_card_flipped else card.front_side
        keyboard = create_card_buttons(card.id, user_state.is_card_flipped)
        await bot.edit_message_text(
            text=text,
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            reply_markup=keyboard,
        )
    elif action == "mark_studied":
        card.is_studied = True
        connection.commit()
        await send_next_card(callback_query, connection, user_id, bot)
    elif action == "next":
        await send_next_card(callback_query, connection, user_id, bot)


async def send_next_card(callback_query, session, user_id, bot: Bot):
    user_state = session.query(UserStateEntity).filter_by(user_id=user_id).first()
    card = (
        session.query(Card)
        .filter(
            Card.user_id == user_id,
            Card.is_studied == False,
            Card.id != user_state.current_card_id,
        )
        .first()
    )

    if not card:
        await callback_query.message.edit_text("No more cards to train!")
        return

    # Update user state
    user_state = session.query(UserStateEntity).filter_by(user_id=user_id).first()
    user_state.current_card_id = card.id
    user_state.is_card_flipped = False
    session.commit()

    # Display next card
    keyboard = create_card_buttons(card.id, is_card_flipped=False)
    await bot.edit_message_text(
        text=card.front_side,
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        reply_markup=keyboard,
    )
