from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton


class RemoveKeyboard(object):
    @staticmethod
    def get_keyboard():
        return ReplyKeyboardRemove()
