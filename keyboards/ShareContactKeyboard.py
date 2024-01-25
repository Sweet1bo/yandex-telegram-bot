from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


class ShareContactKeyboard(object):
    @staticmethod
    def get_keyboard():
        markup = ReplyKeyboardMarkup()
        markup.add(KeyboardButton('Отправить номер телефона', True))

        return markup
