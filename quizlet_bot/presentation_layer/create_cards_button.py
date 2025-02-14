from aiogram import Router, F
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from entity_layer.states_enum import StatesEnum
from filter_layer.user_state_filter import UserStateFilter
from service_layer.card_service import CardService
from service_layer.user_service import UserService
from ui_layer.keyboards.create_cards_keyboards import CreateCardsKeyboards
from ui_layer.keyboards.start_command_keyboards import StartCommandKeyboards
from ui_layer.lexicon.lexicon_ru import lexicon_ru

router = Router()


@router.message(
    F.text == lexicon_ru["keyboards"]["start_keyboard"]["create_cards"]
)
async def handle_create_cards_button(message: Message, db: AsyncSession):
    user_id = str(message.from_user.id)
    user_service = UserService(db)

    await user_service.update_user_state(user_id, StatesEnum.CREATING_CARDS.value)

    await message.reply(
        text=lexicon_ru["create_cards"]["entry"],
        reply_markup=CreateCardsKeyboards.select_mode_for_creating(),
    )


@router.message(
    F.text == lexicon_ru["keyboards"]["create_cards_keyboards"]["manual"],
    UserStateFilter(StatesEnum.CREATING_CARDS.value)
)
async def handle_add_manual_button(message: Message, db: AsyncSession):
    user_id = str(message.from_user.id)
    user_service = UserService(db)
    success = await user_service.update_user_state(
        user_id, StatesEnum.AWAITING_FRONT.value
    )
    if success:
        await message.reply(lexicon_ru["create_cards"]["face_input"])
    else:
        await message.reply(lexicon_ru["create_cards"]["error"])


@router.message(
    F.text == lexicon_ru["keyboards"]["create_cards_keyboards"]["auto"],
    UserStateFilter(StatesEnum.CREATING_CARDS.value)
)
async def handle_add_auto_button(message: Message, db: AsyncSession):
    user_id = str(message.from_user.id)
    user_service = UserService(db)
    success = await user_service.update_user_state(
        user_id, StatesEnum.UPLOADING_CARDS_SETS.value
    )
    if success:
        await message.reply(text=lexicon_ru["create_cards"]["auto_mode"])
    else:
        await message.reply(lexicon_ru["create_cards"]["error"])


@router.message(
    F.text == lexicon_ru["keyboards"]["create_cards_keyboards"]["finish_uploading_session"],
    UserStateFilter(StatesEnum.UPLOADING_CARDS_SETS.value),
)
async def finish_adding_sets(message: Message, db: AsyncSession):
    user_id = str(message.from_user.id)
    user_service = UserService(db)
    await user_service.update_user_state(user_id, StatesEnum.ZERO_STATE.value)
    await message.reply(
        text=lexicon_ru["create_cards"]["auto_mode_exit"],
        reply_markup=StartCommandKeyboards.startup_card_builder(),
    )


@router.message(UserStateFilter(StatesEnum.UPLOADING_CARDS_SETS.value))
async def handle_added_set(message: Message, db: AsyncSession):
    user_id = str(message.from_user.id)
    card_service = CardService(db)
    success = await card_service.add_user_set(user_id, message.text)
    await message.reply(
        text=success, reply_markup=CreateCardsKeyboards.leave_mode_for_creating()
    )
