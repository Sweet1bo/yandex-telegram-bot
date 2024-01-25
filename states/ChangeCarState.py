from aiogram.dispatcher.filters.state import StatesGroup, State


class ChangeCarState(StatesGroup):
    name = State()
    photo = State()