import asyncio
import logging
import datetime
from aiogram import Bot

from netschool_api import fetch_homework_for_group
from config import GROUP_CREDENTIALS
from bot_settings import get_channel_id, get_send_time

logging.basicConfig(level=logging.INFO)

async def send_daily_homework(bot: Bot):
    channel_id = get_channel_id()
    if channel_id is None:
        return

    tomorrow = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%d.%m.%Y")
    parts = [f"<b>ДОМАШНЕЕ ЗАДАНИЕ НА <u>{tomorrow}</u></b>\n"]

    for group_name in GROUP_CREDENTIALS.keys():
        hw_text = await fetch_homework_for_group(group_name)

        hw_text = hw_text.split("\n")
        hw_text.pop(0)
        hw_text.pop(1)

        parts.append("\n".join(hw_text))

    final_text = "\n\n".join(parts)

    try:
        await bot.send_message(chat_id=channel_id, text=final_text)
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
            await send_daily_homework(bot)
            await asyncio.sleep(60)