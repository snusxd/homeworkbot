import asyncio
import logging
import datetime

from aiogram import Bot

from .netschool_api import fetch_homework_for_group
from .config import GROUP_CREDENTIALS
from .bot_settings import *

logging.basicConfig(level=logging.INFO)

async def attempt_send_daily_homework(bot: Bot):
    while True:
        last_time = get_last_bot_message_time()
        now = datetime.datetime.now()

        if last_time is not None:
            delta = now - last_time
            if delta.total_seconds() < 120:
                set_last_bot_message_time(now)
                break
            else:
                await send_new_message(bot)
        else:
            await send_new_message(bot)


async def send_new_message(bot: Bot):
    channel_id = get_channel_id()
    if channel_id is None:
        return

    tomorrow = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%d.%m.%Y")
    parts = [f"<b>ДОМАШНЕЕ ЗАДАНИЕ НА <u>{tomorrow}</u></b>\n"]

    for group_name in GROUP_CREDENTIALS.keys():
        hw_text = await fetch_homework_for_group(group_name, day="tomorrow")

        hw_text = hw_text.split("\n")
        hw_text.pop(0)
        hw_text.pop(1)

        parts.append("\n".join(hw_text))

    final_text = "\n\n".join(parts)

    try:
        await bot.send_message(chat_id=channel_id, text=final_text)
        set_last_bot_message_time(datetime.datetime.now())
    except Exception as e:
        logging.error(f"Не смогли отправить сообщение в канал: {e}")


async def scheduler_loop(bot: Bot):
    while True:
        await asyncio.sleep(30)
        send_time = get_send_time()
        if send_time is None:
            continue

        now = datetime.datetime.now().strftime("%H:%M")
        if now == send_time:
            await attempt_send_daily_homework(bot)
            await asyncio.sleep(60)