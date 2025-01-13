from aiogram.fsm.state import StatesGroup, State

class AdminStates(StatesGroup):
    waiting_for_channel_link = State()
    check_channel_permissions = State()
    waiting_for_time = State()

class UserStates(StatesGroup):
    choose_group = State()