import re
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from config.config import ADMIN_ID
from .states import AdminStates
from .keyboards import admin_menu_kb
from config.bot_settings import *

router = Router()

@router.message(Command("admin"))
async def cmd_admin(message: Message):
    if message.from_user.id != ADMIN_ID:
        await message.reply("Команда доступна только администратору!")
        return
    text = "Добро пожаловать в админ-меню!"
    await message.answer(text, reply_markup=admin_menu_kb())

@router.callback_query(F.data == "select_channel")
async def callback_select_channel(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id != ADMIN_ID:
        return
    await state.set_state(AdminStates.waiting_for_channel_link)

    await callback.message.edit_text(
        "Перешлите любое сообщение с канала, для рассылки!"
    )

@router.message(AdminStates.waiting_for_channel_link)
async def process_forwarded_message(message: Message, state: FSMContext):
    if message.from_user.id != ADMIN_ID:
        return
    
    fwd_chat = message.forward_from_chat
    if not fwd_chat:
        await message.reply("Похоже, это не пересланное сообщение из канала. Попробуйте ещё раз.")
        return

    channel_id = fwd_chat.id
    set_channel_id(channel_id)

    await message.reply(
        f"Выбрано! `CHANNEL_ID` выбранного чата: {channel_id}",
        parse_mode="Markdown"
    )
    await state.clear()

@router.callback_query(F.data == "select_time")
async def callback_select_time(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id != ADMIN_ID:
        return
    await state.set_state(AdminStates.waiting_for_time)
    await callback.message.edit_text("Напишите время для рассылки в формате ЧЧ:ММ")

@router.message(AdminStates.waiting_for_time)
async def process_select_time(message: Message, state: FSMContext):
    if message.from_user.id != ADMIN_ID:
        return

    text = message.text.strip()
    pattern = r"^\d{2}:\d{2}$"
    if not re.match(pattern, text):
        await message.reply("Время написано некорректно, повторите ещё раз.")
        return

    hh, mm = text.split(":")
    try:
        hh_i = int(hh)
        mm_i = int(mm)
        if not (0 <= hh_i <= 23 and 0 <= mm_i <= 59):
            raise ValueError
    except ValueError:
        await message.reply("Время написано некорректно, повторите ещё раз.")
        return

    set_send_time(text)
    await message.reply(f"Отлично! Время рассылки установлено на {text}")
    await state.clear()

@router.callback_query(F.data == "view_settings")
async def callback_view_settings(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        return

    channel_id = get_channel_id()
    send_time = get_send_time()

    channel_str = str(channel_id) if channel_id is not None else "Не выбран"
    time_str = send_time if send_time is not None else "Не установлено"

    text = (
        f"ID выбранного канала: {channel_str}\n"
        f"Выбранное время рассылки: {time_str}"
    )

    await callback.message.edit_text(text, reply_markup=admin_menu_kb())