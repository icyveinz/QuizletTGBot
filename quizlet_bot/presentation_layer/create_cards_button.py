from aiogram import Router, F
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from entity_layer.states_enum import StatesEnum
from filter_layer.user_state_filter import UserStateFilter
from service_layer.user_service import UserService
from ui_layer.create_cards_keyboards import CreateCardsKeyboards

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
    await message.reply(text="Выбран автоматический режим для загрузки\nЗагрузите пары разделенные символом ")
