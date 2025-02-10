from aiogram import Router, F
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from entity_layer.states_enum import StatesEnum
from filter_layer.user_state_filter import UserStateFilter
from service_layer.card_service import CardService
from service_layer.user_service import UserService
from ui_layer.create_cards_keyboards import CreateCardsKeyboards
from ui_layer.start_command_keyboards import StartCommandKeyboards

router = Router()


@router.message(F.text == "Create Cards")
async def handle_create_cards_button(message: Message, db: AsyncSession):
    user_id = str(message.from_user.id)
    user_service = UserService(db)

    await user_service.update_user_state(user_id, StatesEnum.CREATING_CARDS.value)

    await message.reply(
        text="Выберите режим с помощью которого хотели бы загрузить новые слова",
        reply_markup=CreateCardsKeyboards.select_mode_for_creating(),
    )


@router.message(
    F.text == "Добавить вручную", UserStateFilter(StatesEnum.CREATING_CARDS.value)
)
async def handle_add_manual_button(message: Message, db: AsyncSession):
    user_id = str(message.from_user.id)
    user_service = UserService(db)
    success = await user_service.update_user_state(
        user_id, StatesEnum.AWAITING_FRONT.value
    )
    if success:
        await message.reply("Введите лицевую сторону карты")
    else:
        await message.reply("Произошла ошибка, попробуйте позже")


@router.message(
    F.text == "Загрузить пакетом", UserStateFilter(StatesEnum.CREATING_CARDS.value)
)
async def handle_add_auto_button(message: Message, db: AsyncSession):
    user_id = str(message.from_user.id)
    user_service = UserService(db)
    success = await user_service.update_user_state(
        user_id, StatesEnum.UPLOADING_CARDS_SETS.value
    )
    if success:
        await message.reply(text="Выбран автоматический режим для загрузки\nЗагрузите пары разделенные символом <b>'-.-'</b>\nКаждая новая строчка должна начинаться с новой строки")
    else:
        await message.reply("Произошла ошибка, попробуйте позже")


@router.message(F.text == "Завершить добавление", UserStateFilter(StatesEnum.UPLOADING_CARDS_SETS.value))
async def finish_adding_sets(message: Message, db: AsyncSession):
    user_id = str(message.from_user.id)
    user_service = UserService(db)
    await user_service.update_user_state(user_id, StatesEnum.ZERO_STATE.value)
    await message.reply(text="Вы вышли из режима автоматического добавления карт", reply_markup=StartCommandKeyboards.start_creating_cards())

@router.message(UserStateFilter(StatesEnum.UPLOADING_CARDS_SETS.value))
async def handle_added_set(message: Message, db: AsyncSession):
    user_id = str(message.from_user.id)
    card_service = CardService(db)
    success = await card_service.add_user_set(user_id, message.text)
    await message.reply(text=success, reply_markup=CreateCardsKeyboards.leave_mode_for_creating())

