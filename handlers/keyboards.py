from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def choose_group_initial_kb():
    kb = [
        [InlineKeyboardButton(text="Выбрать свою группу", callback_data="choose_group")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)

def main_menu_kb():
    kb = [
        [InlineKeyboardButton(text="Посмотреть ДЗ на завтра", callback_data="view_homework")],
        [InlineKeyboardButton(text="Изменить свою группу", callback_data="choose_group")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)

def group_menu_kb():
    kb = [
        [
            InlineKeyboardButton(text="Инфотех (1)", callback_data="group_infotech1"),
            InlineKeyboardButton(text="Инфотех (2)", callback_data="group_infotech2"),
        ],
        [InlineKeyboardButton(text="Химбио", callback_data="group_himbio")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)



def admin_menu_kb():
    kb = [
        [InlineKeyboardButton(text="Выбрать канал для рассылки", callback_data="select_channel")],
        [InlineKeyboardButton(text="Выбрать время рассылки", callback_data="select_time")],
        [InlineKeyboardButton(text="Просмотреть выбранные настройки", callback_data="view_settings")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)


def check_channel_kb():
    kb = [
        [InlineKeyboardButton(text="Готово", callback_data="channel_ready")],
        [InlineKeyboardButton(text="Проверить ещё раз", callback_data="channel_not_ready")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)
