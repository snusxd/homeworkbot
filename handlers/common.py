import asyncio
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from database.users_database import save_user_data, load_user_group
from config.users_data import get_user_group, set_user_group
from .states import UserStates
from .keyboards import (
    choose_group_initial_kb,
    main_menu_kb,
    group_menu_kb,
    day_choice_kb,
    back_to_main_kb
)
from config.netschool_api import fetch_homework_for_group

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    user_id = message.from_user.id
    group_name = get_user_group(user_id)

    if group_name is None:
        await message.answer(
            "Ты ещё не выбрал группу. Нажми на кнопку ниже!",
            reply_markup=choose_group_initial_kb()
        )
    else:
        await message.answer(
            "Добро пожаловать! 😉",
            reply_markup=main_menu_kb()
        )


@router.callback_query(F.data == "choose_group")
async def callback_choose_group(callback: CallbackQuery, state: FSMContext):
    await state.set_state(UserStates.choose_group)
    await callback.message.edit_text(
        text="Выбери свою группу:",
        reply_markup=group_menu_kb()
    )


@router.callback_query(UserStates.choose_group, F.data.in_({"group_infotech1", "group_infotech2", "group_himbio"}))
async def callback_confirm_group(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id

    group = load_user_group(user_id)

    if callback.data == "group_infotech1":
        group = "Инфотех (1)"
    elif callback.data == "group_infotech2":
        group = "Инфотех (2)"
    else:
        group = "Химбио"

    save_user_data(user_id, group)
    
    await state.clear()

    if group is None:
        await callback.message.edit_text(
            text="Добро пожаловать! 😉",
            reply_markup=main_menu_kb()
        )
    else:
        await callback.message.edit_text(
            text="Группа успешно изменена!\nТеперь выбери действие! 😊",
            reply_markup=main_menu_kb()
        )


@router.callback_query(F.data == "view_homework")
async def callback_view_homework_choice(callback: CallbackQuery):
    user_id = callback.from_user.id
    group_name = get_user_group(user_id)

    if group_name is None:
        await callback.message.edit_text(
            text="Сначала выбери свою группу!",
            reply_markup=group_menu_kb()
        )
        return

    await callback.message.edit_text(
        text="Какой день интересует?",
        reply_markup=day_choice_kb()
    )


@router.callback_query(F.data.in_({"dz_today", "dz_tomorrow"}))
async def callback_view_homework_for_day(callback: CallbackQuery):
    user_id = callback.from_user.id
    group_name = get_user_group(user_id)

    if group_name is None:
        await callback.message.edit_text(
            text="Сначала выбери свою группу!",
            reply_markup=group_menu_kb()
        )
        return

    if callback.data == "dz_today":
        day = "today"
    else:
        day = "tomorrow"

    hw_text = await fetch_homework_for_group(group_name, day=day)

    await callback.message.edit_text(
        text=hw_text,
        reply_markup=back_to_main_kb()
    )

@router.callback_query(F.data == "back_to_main")
async def callback_back_to_main(callback: CallbackQuery):
    await callback.message.edit_text(
        text="Добро пожаловать! 😉",
        reply_markup=main_menu_kb()
    )