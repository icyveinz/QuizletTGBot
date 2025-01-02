from aiogram import types
from sqlalchemy.exc import SQLAlchemyError
from controller import get_db
from model import Card, UserStateEntity
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

async def start_command(message: types.Message):
    user_id = str(message.from_user.id)
    session = next(get_db())

    try:
        # Check if user has cards
        user_cards = session.query(Card).filter(Card.user_id == user_id).all()

        if user_cards:
            keyboard = ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text="View Cards"), KeyboardButton(text="Create Cards"), KeyboardButton(text="Train Cards")]
                ],
                resize_keyboard=True
            )
            await message.reply(
                "Welcome back! You already have cards. Use the buttons below to view or create more.",
                reply_markup=keyboard
            )
        else:
            keyboard = ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text="Create Cards")]
                ],
                resize_keyboard=True
            )
            await message.reply(
                "You don't have any cards yet. Would you like to create your first cards?",
                reply_markup=keyboard
            )

        # Initialize user state if not present
        user_state = session.query(UserStateEntity).filter_by(user_id=user_id).first()
        if not user_state:
            new_state = UserStateEntity(user_id=user_id, is_card_flipped=False)
            session.add(new_state)
            session.commit()
    except SQLAlchemyError as e:
        await message.reply("An error occurred while accessing the database. Please try again later.")
        print(f"Database error: {e}")
    finally:
        session.close()

# Handler for "Create Cards" button
async def handle_create_cards_button(message: types.Message):
    user_id = str(message.from_user.id)
    session = next(get_db())

    try:
        user_state = session.query(UserStateEntity).filter_by(user_id=user_id).first()
        if user_state:
            user_state.state = "AWAITING_FRONT"
            session.commit()

            await message.reply("Please enter the front side of the card.")
        else:
            await message.reply("An error occurred. Please try again later.")
    except SQLAlchemyError as e:
        await message.reply("An error occurred while updating your state. Please try again later.")
        print(f"Database error: {e}")
    finally:
        session.close()

# Handler for card input
async def handle_card_input(message: types.Message):
    user_id = str(message.from_user.id)
    session = next(get_db())

    try:
        user_state = session.query(UserStateEntity).filter_by(user_id=user_id).first()

        if not user_state or not user_state.state:
            await message.reply("Please press the 'Create Cards' button first to create a card.")
            return

        if user_state.state == "AWAITING_FRONT":
            # Save the front text
            user_state.front_side = message.text.strip()
            user_state.state = "AWAITING_BACK"
            session.commit()

            await message.reply("Front side saved! Now, please enter the back side of the card.")

        elif user_state.state == "AWAITING_BACK":
            # Save the back text and create card
            back = message.text.strip()
            front = user_state.front_side

            new_card = Card(front_side=front, back_side=back, user_id=user_id)
            session.add(new_card)
            session.commit()

            # Reset user state
            user_state.state = None
            user_state.front_side = None
            user_state.back_side = None
            session.commit()

            await message.reply(f"Card created!\nFront: {front}\nBack: {back}")
        else:
            await message.reply("Unexpected state. Please press the 'Create Cards' button again to restart.")
    except SQLAlchemyError as e:
        await message.reply("An error occurred while saving the card. Please try again later.")
        print(f"Database error: {e}")
    finally:
        session.close()