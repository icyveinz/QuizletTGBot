from aiogram import types, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from sqlalchemy.exc import SQLAlchemyError
from controller import get_db
from model import Card, UserState, StateEnum
from tools import int_to_str

# Global variable to track user state (for simplicity; a proper state machine is preferred)
user_states = {}

# /start command
async def start_command(message: types.Message):
    user_id = message.from_user.id
    session = next(get_db())

    try:
        user_cards = session.query(Card).filter(Card.user_id == user_id).all()

        if user_cards:
            await message.reply("Welcome back! You already have cards. Use /view_cards to see them.")
        else:
            keyboard = ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text="Create Cards")],
                ],
                resize_keyboard=True
            )
            await message.reply(
                "You don't have any cards yet. Would you like to create your first cards?",
                reply_markup=keyboard
            )
    except SQLAlchemyError as e:
        await message.reply("An error occurred while accessing the database. Please try again later.")
        print(f"Database error: {e}")
    finally:
        session.close()


# Handler for "Create Cards" button
async def handle_create_cards_button(message: types.Message):
    user_id = message.from_user.id
    user_states[user_id] = UserState(state=StateEnum.AWAITING_FRONT, front="")  # Set state and initialize temp data
    await message.reply("Please enter the front side of the card.")


# Handler for card input
async def handle_card_input(message: types.Message):
    user_id = message.from_user.id
    user_data : UserState = user_states.get(user_id)

    if not user_data:
        await message.reply("Please press the 'Create Cards' button first to create a card.")
        return

    # Handle input based on the current state
    if user_data.state == StateEnum.AWAITING_FRONT:
        # Save the front text
        user_data.front = message.text.strip()
        user_data.state = StateEnum.AWAITING_BACK
        await message.reply("Front side saved! Now, please enter the back side of the card.")

    elif user_data.state == StateEnum.AWAITING_BACK:
        # Save the back text
        back = message.text.strip()
        front = user_data.front
        try:
            # Save the card to the database
            session = next(get_db())
            new_card = Card(main_side=front, reverse_side=back, user_id=int_to_str(user_id))
            session.add(new_card)
            session.commit()
            session.close()

            # Reset user state
            user_states[user_id] = None

            await message.reply(f"Card created!\nFront: {front}\nBack: {back}")
        except SQLAlchemyError as e:
            await message.reply("An error occurred while saving the card. Please try again later.")
            print(f"Database error: {e}")
        finally:
            user_states[user_id] = None  # Reset state
    else:
        await message.reply("Unexpected state. Please press the 'Create Cards' button again to restart.")

# Register handlers
def register_start_command(dp: Dispatcher):
    dp.message.register(start_command, CommandStart())
    dp.message.register(handle_create_cards_button, lambda message: message.text == "Create Cards")
    dp.message.register(handle_card_input)