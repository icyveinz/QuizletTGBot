from aiogram import types
from sqlalchemy.exc import SQLAlchemyError
from controller import get_db
from model import Card


async def reset_trained_cards_route(message: types.Message):
    connection = next(get_db())
    user_id = message.from_user.id
    try:
        cards = (
            connection
            .query(Card)
            .filter_by(user_id=user_id, is_studied=True)
            .update(
                {'is_studied': False},
                synchronize_session='fetch'
            )
        )
        connection.commit()
        await message.reply(
            f"{cards} were reset so you could repeat it again"
        )
    except SQLAlchemyError as e:
        await message.reply(f"Unexpected error: {e}")
    finally:
        connection.close()